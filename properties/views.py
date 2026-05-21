import io
import re
import pandas as pd
from django.db import models
from django.db import transaction
from django.db.models import Avg, Count, Min, Max
from django.core.cache import cache
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.http import HttpResponse
from rest_framework import filters, viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, inline_serializer

from .cache_utils import bump_property_cache_version, make_property_cache_key
from .models import (
    Amenity, Category, District, FavoriteProperty, Property, PropertyImage, Ward,
    ViewingAppointment, ComparisonList, PropertyManager
)
from .serializers import (
    AmenitySerializer,
    CategorySerializer,
    DistrictSerializer,
    PropertyImageSerializer,
    PropertySerializer,
    WardSerializer,
    FavoritePropertySerializer,
    ViewingAppointmentSerializer,
    ComparisonListSerializer,
)
from .permissions import IsAppointmentParticipant
from .tasks import send_appointment_email_task


# --- HÀM HỖ TRỢ XỬ LÝ KÝ TỰ LỖI CHO EXCEL ---
def clean_for_excel(value):
    if not isinstance(value, str):
        return value
    illegal_chars_re = re.compile(
        r'[\000-\010]|[\013-\014]|[\016-\037]|[\x00-\x1f\x7f-\x9f]|[\ufffe-\uffff]'
    )
    return illegal_chars_re.sub("", value)


# Metadata ViewSets: chỉ đọc công khai (GET), ghi (POST/PUT/DELETE) yêu cầu Admin
@extend_schema(tags=["Metadata Lookup"])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]


@extend_schema(tags=["Metadata Lookup"])
class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all().order_by("name")
    serializer_class = DistrictSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]


@extend_schema(tags=["Metadata Lookup"])
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(name="district", description="Lọc theo ID của Quận/Huyện", required=False, type=int),
        ]
    )
)
class WardViewSet(viewsets.ModelViewSet):
    queryset = Ward.objects.select_related("district").all().order_by("district__name", "name")
    serializer_class = WardSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        queryset = super().get_queryset()
        district_id = self.request.query_params.get("district")
        if district_id:
            queryset = queryset.filter(district_id=district_id)
        return queryset


@extend_schema(tags=["Metadata Lookup"])
class AmenityViewSet(viewsets.ModelViewSet):
    queryset = Amenity.objects.all().order_by("name")
    serializer_class = AmenitySerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]


@extend_schema(tags=["Real Estate Core"])
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(name="search", description="Tìm kiếm toàn văn (Full-text Search) theo tiêu đề, mô tả, địa chỉ", required=False, type=str),
            OpenApiParameter(name="source", description="Lọc theo nguồn tin (ví dụ: NhaTot, Chotot)", required=False, type=str),
            OpenApiParameter(name="district", description="Lọc theo tên Quận/Huyện", required=False, type=str),
            OpenApiParameter(name="min_price", description="Giá tối thiểu (VNĐ)", required=False, type=int),
            OpenApiParameter(name="max_price", description="Giá tối đa (VNĐ)", required=False, type=int),
            OpenApiParameter(name="min_area", description="Diện tích tối thiểu (m2)", required=False, type=float),
            OpenApiParameter(name="max_area", description="Diện tích tối đa (m2)", required=False, type=float),
            OpenApiParameter(name="is_active", description="Trạng thái hoạt động (true/false)", required=False, type=str),
            OpenApiParameter(name="in_bbox", description="Lọc địa lý Bounding Box (định dạng: min_lon,min_lat,max_lon,max_lat)", required=False, type=str),
        ]
    )
)
class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["price", "area", "price_per_m2", "created_at"]
    ordering = ["-created_at"]
    cache_timeout = 60 * 5

    def get_queryset(self):
        queryset = (
            Property.objects.select_related("category", "district", "ward")
            .prefetch_related("amenities", "images")
            .all()
        )

        # 1. Full-text Search (Task 11)
        search_query = self.request.query_params.get("search")
        if search_query:
            vector = (
                    SearchVector("title", weight="A") +
                    SearchVector("address", weight="B") +
                    SearchVector("description", weight="C")
            )
            query = SearchQuery(search_query)
            queryset = queryset.annotate(
                rank=SearchRank(vector, query)
            ).filter(rank__gte=0.05).order_by("-rank")

        # 2. Bộ lọc lọc dữ liệu (Task 5)
        source = self.request.query_params.get("source")
        district = self.request.query_params.get("district")
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")
        min_area = self.request.query_params.get("min_area")
        max_area = self.request.query_params.get("max_area")
        is_active = self.request.query_params.get("is_active")

        if source:
            queryset = queryset.filter(source_name__iexact=source)
        if district:
            queryset = queryset.filter(district__name__icontains=district)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if min_area:
            queryset = queryset.filter(area__gte=min_area)
        if max_area:
            queryset = queryset.filter(area__lte=max_area)
        if is_active in ["true", "false"]:
            queryset = queryset.filter(is_active=is_active == "true")

        # --- TASK 13: LỌC THEO VÙNG BẢN ĐỒ (BOUNDING BOX) ---
        # User kéo bản đồ đến đâu, chỉ lấy tọa độ trong vùng đó
        in_bbox = self.request.query_params.get("in_bbox")
        if in_bbox:
            # Format: min_lon,min_lat,max_lon,max_lat
            try:
                lon1, lat1, lon2, lat2 = map(float, in_bbox.split(","))
                queryset = queryset.filter(
                    longitude__gte=lon1, longitude__lte=lon2,
                    latitude__gte=lat1, latitude__lte=lat2
                )
            except ValueError:
                pass

        return queryset

    # --- TASK 13: MAP DATA ACTION ---
    @action(detail=False, methods=["get"])
    def map_data(self, request):
        """Trả về dữ liệu cực nhẹ phục vụ hiển thị Marker trên bản đồ"""
        # Chỉ lấy những bài có tọa độ
        queryset = self.get_queryset().filter(latitude__isnull=False, longitude__isnull=False)

        # Chỉ lấy các trường cần thiết để giảm tải dung lượng mạng
        data = queryset.values('id', 'title', 'price', 'latitude', 'longitude', 'category__name')

        return Response(data)

    # --- TASK 12: EXPORT EXCEL ACTION ---
    @extend_schema(tags=["Analytics & Reporting"])
    @action(detail=False, methods=["get"], url_path='export_excel')
    def export_excel(self, request):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "Không có dữ liệu để xuất."}, status=400)

        data = []
        for p in queryset:
            date_str = p.created_at.strftime("%d/%m/%Y") if p.created_at else ""
            data.append({
                "Tiêu đề": clean_for_excel(p.title),
                "Giá (VNĐ)": p.price,
                "Diện tích (m2)": p.area,
                "Quận": clean_for_excel(p.district.name) if p.district else "",
                "Nguồn": p.source_name,
                "Link gốc": p.source_url,
                "Ngày đăng": date_str,
            })

        df = pd.DataFrame(data)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Danh sách phòng trọ')

        output.seek(0)
        response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=danh_sach_phong_tro.xlsx'
        return response

    @extend_schema(tags=["Analytics & Reporting"])
    @action(detail=False, methods=["get"])
    def stats(self, request):
        cache_key = make_property_cache_key("stats", request.query_params)
        data = cache.get(cache_key)
        if data is None:
            queryset = self.get_queryset()
            data = queryset.aggregate(
                total=Count("id"), min_price=Min("price"), max_price=Max("price"),
                avg_price=Avg("price"), min_area=Min("area"), max_area=Max("area"), avg_area=Avg("area"),
            )
            cache.set(cache_key, data, self.cache_timeout)
            data["cache"] = "miss"
        else:
            data["cache"] = "hit"
        return Response(data)

    @extend_schema(tags=["System Administration"], request=None)
    @action(detail=False, methods=["post"], permission_classes=[IsAdminUser])
    def clear_cache(self, request):
        version = bump_property_cache_version()
        return Response({"detail": "Property cache cleared.", "cache_version": version})

    @extend_schema(tags=["Favorites"], request=None)
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        """Yêu thích hoặc hủy yêu thích một tin đăng phòng trọ (Toggle)"""
        property_obj = self.get_object()
        fav, created = FavoriteProperty.objects.get_or_create(user=request.user, property=property_obj)
        if not created:
            fav.delete()
            return Response({"detail": "Đã xóa khỏi danh sách yêu thích."}, status=status.HTTP_200_OK)
        return Response({"detail": "Đã thêm vào danh sách yêu thích."}, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Analytics & Reporting"])
    @action(detail=False, methods=["get"], url_path="district-stats")
    def district_stats(self, request):
        """Thống kê chi tiết số tin đăng và mức giá/diện tích trung bình theo từng Quận/Huyện"""
        stats = Property.objects.values("district__name").annotate(
            total_listings=Count("id"),
            avg_price=Avg("price"),
            avg_price_per_m2=Avg("price_per_m2"),
            avg_area=Avg("area")
        ).filter(district__name__isnull=False).order_by("-total_listings")
        return Response(stats)


@extend_schema(tags=["Metadata Lookup"])
class PropertyImageViewSet(viewsets.ModelViewSet):
    queryset = PropertyImage.objects.select_related("property").all()
    serializer_class = PropertyImageSerializer

    def get_permissions(self):
        # Xem ảnh: công khai. Upload/xóa ảnh: yêu cầu đăng nhập
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]


@extend_schema(tags=["Favorites"])
class FavoritePropertyViewSet(viewsets.ReadOnlyModelViewSet):
    """Danh sách các tin đăng phòng trọ đã lưu của người dùng hiện tại"""
    permission_classes = [IsAuthenticated]
    serializer_class = FavoritePropertySerializer

    def get_queryset(self):
        return FavoriteProperty.objects.filter(user=self.request.user).select_related("property")


@extend_schema(tags=["Booking & Appointments"])
class ViewingAppointmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet quản lý lịch hẹn xem phòng trọ.
    - Khách thuê (Guest) có thể tạo lịch hẹn, xem và hủy lịch hẹn của mình.
    - Chủ trọ (Landlord) có thể xem, xác nhận, hủy hoặc hoàn thành lịch hẹn cho phòng trọ của họ.
    """
    serializer_class = ViewingAppointmentSerializer
    permission_classes = [IsAuthenticated, IsAppointmentParticipant]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "is_staff", False):
            return ViewingAppointment.objects.select_related("guest", "landlord", "property").all()
        # Lọc danh sách lịch hẹn: Guest thấy lịch họ đặt, Landlord thấy lịch của phòng họ quản lý
        return ViewingAppointment.objects.select_related("guest", "landlord", "property").filter(
            models.Q(guest=user) | models.Q(landlord=user)
        )

    def perform_create(self, serializer):
        property_obj = serializer.validated_data["property"]
        # Chủ nhà được lấy từ bảng mapping PropertyManager
        try:
            landlord = property_obj.manager.landlord
        except PropertyManager.DoesNotExist:
            raise PermissionDenied(
                "Phòng trọ này chưa được gán cho chủ trọ nào. Không thể đặt lịch hẹn."
            )

        # Sử dụng transaction.atomic để đảm bảo dữ liệu ghi nhất quán
        with transaction.atomic():
            instance = serializer.save(guest=self.request.user, landlord=landlord)
            # Gọi Celery Task gửi email thông báo ngầm dưới nền
            send_appointment_email_task.delay(instance.id)  # type: ignore

    def perform_update(self, serializer):
        instance = self.get_object()
        new_status = serializer.validated_data.get("status", instance.status)

        # Ràng buộc nghiệp vụ: Chỉ chủ nhà/admin mới được chuyển trạng thái thành CONFIRMED hoặc COMPLETED
        if new_status in ["CONFIRMED", "COMPLETED"]:
            if not (self.request.user == instance.landlord or getattr(self.request.user, "is_staff", False)):
                raise PermissionDenied("Chỉ chủ trọ mới có quyền xác nhận hoặc hoàn thành lịch hẹn xem phòng.")

        with transaction.atomic():
            updated_instance = serializer.save()
            # Gửi email thông báo cập nhật lịch xem phòng qua Celery
            send_appointment_email_task.delay(updated_instance.id)  # type: ignore


@extend_schema(tags=["Property Comparison"])
class ComparisonViewSet(viewsets.ViewSet):
    """
    ViewSet quản lý danh sách so sánh phòng trọ của người dùng.
    """
    permission_classes = [IsAuthenticated]

    def get_comparison_list(self, user):
        # Tự động khởi tạo ComparisonList cho user nếu chưa tồn tại
        comp_list, _ = ComparisonList.objects.get_or_create(user=user)
        return comp_list

    @action(detail=False, methods=["get"], url_path="list")
    def retrieve_list(self, request):
        """Lấy danh sách các phòng trọ đang so sánh hiện tại"""
        comp_list = self.get_comparison_list(request.user)
        serializer = ComparisonListSerializer(comp_list)
        return Response(serializer.data)

    @extend_schema(
        request=inline_serializer(
            name="ComparisonAddRequest",
            fields={
                "property_id": serializers.IntegerField(help_text="ID của phòng trọ cần thêm vào danh sách so sánh")
            }
        ),
        responses={200: ComparisonListSerializer}
    )
    @action(detail=False, methods=["post"], url_path="add")
    def add_property(self, request):
        """Thêm phòng trọ vào danh sách so sánh"""
        property_id = request.data.get("property_id")
        if not property_id:
            return Response({"error": "Vui lòng cung cấp property_id."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            property_obj = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            return Response({"error": "Không tìm thấy phòng trọ."}, status=status.HTTP_404_NOT_FOUND)

        comp_list = self.get_comparison_list(request.user)
        comp_list.properties.add(property_obj)
        
        # Xóa Cache so sánh của user do danh sách đã thay đổi
        cache.delete(f"compare_matrix_{request.user.id}")

        serializer = ComparisonListSerializer(comp_list)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=inline_serializer(
            name="ComparisonRemoveRequest",
            fields={
                "property_id": serializers.IntegerField(help_text="ID của phòng trọ cần xóa khỏi danh sách so sánh")
            }
        ),
        responses={200: ComparisonListSerializer}
    )
    @action(detail=False, methods=["post"], url_path="remove")
    def remove_property(self, request):
        """Xóa phòng trọ khỏi danh sách so sánh"""
        property_id = request.data.get("property_id")
        if not property_id:
            return Response({"error": "Vui lòng cung cấp property_id."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            property_obj = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            return Response({"error": "Không tìm thấy phòng trọ."}, status=status.HTTP_404_NOT_FOUND)

        comp_list = self.get_comparison_list(request.user)
        comp_list.properties.remove(property_obj)  # Fix: dùng object thay vì raw ID

        # Xóa Cache so sánh của user
        cache.delete(f"compare_matrix_{request.user.id}")

        serializer = ComparisonListSerializer(comp_list)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="matrix")
    def matrix(self, request):
        """
        Trả về ma trận so sánh chi tiết giữa các phòng trọ của người dùng.
        Đoạn xử lý nặng này được tối ưu hiệu năng bằng Caching qua Redis.
        """
        user = request.user
        cache_key = f"compare_matrix_{user.id}"
        
        # Đọc dữ liệu từ Redis Cache trước
        cached_data = cache.get(cache_key)
        if cached_data:
            cached_data["cache"] = "hit"
            return Response(cached_data)

        comp_list = self.get_comparison_list(user)
        # Tối ưu truy vấn tránh lỗi N+1: Sử dụng select_related và prefetch_related
        properties = comp_list.properties.select_related(
            "category", "district", "ward"
        ).prefetch_related("amenities", "images").all()

        if not properties.exists():
            return Response({"matrix": [], "cache": "miss"})

        # Xây dựng ma trận so sánh dữ liệu
        matrix_data = []
        for prop in properties:
            matrix_data.append({
                "id": prop.id,
                "title": prop.title,
                "price": prop.price,
                "area": prop.area,
                "price_per_m2": prop.price_per_m2,
                "category": prop.category.name,
                "address": f"{prop.address}, {prop.ward.name if prop.ward else ''}, {prop.district.name if prop.district else ''}",
                "amenities": [amenity.name for amenity in prop.amenities.all()],
                "images": [img.image_url for img in prop.images.all()[:3]]
            })

        response_data = {"matrix": matrix_data, "cache": "miss"}
        
        # Lưu vào Redis Cache với TTL là 10 phút (600 giây)
        cache.set(cache_key, response_data, 600)
        
        return Response(response_data)