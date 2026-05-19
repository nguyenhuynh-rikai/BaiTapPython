import io
import re
import pandas as pd
from django.db.models import Avg, Count, Min, Max
from django.core.cache import cache
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.http import HttpResponse
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from .cache_utils import bump_property_cache_version, make_property_cache_key
from .models import Amenity, Category, District, Property, PropertyImage, Ward
from .serializers import (
    AmenitySerializer,
    CategorySerializer,
    DistrictSerializer,
    PropertyImageSerializer,
    PropertySerializer,
    WardSerializer,
)

# --- HÀM HỖ TRỢ XỬ LÝ KÝ TỰ LỖI CHO EXCEL ---
def clean_for_excel(value):
    if not isinstance(value, str):
        return value
    illegal_chars_re = re.compile(
        r'[\000-\010]|[\013-\014]|[\016-\037]|[\x00-\x1f\x7f-\x9f]|[\ufffe-\uffff]'
    )
    return illegal_chars_re.sub("", value)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all().order_by("name")
    serializer_class = DistrictSerializer
    permission_classes = [AllowAny]


class WardViewSet(viewsets.ModelViewSet):
    queryset = Ward.objects.select_related("district").all().order_by("district__name", "name")
    serializer_class = WardSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        district_id = self.request.query_params.get("district")
        if district_id:
            queryset = queryset.filter(district_id=district_id)
        return queryset


class AmenityViewSet(viewsets.ModelViewSet):
    queryset = Amenity.objects.all().order_by("name")
    serializer_class = AmenitySerializer
    permission_classes = [AllowAny]


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
                "Phường": clean_for_excel(p.ward.name) if p.ward else "",
                "Địa chỉ": clean_for_excel(p.address),
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

    @action(detail=False, methods=["post"], permission_classes=[IsAdminUser])
    def clear_cache(self, request):
        version = bump_property_cache_version()
        return Response({"detail": "Property cache cleared.", "cache_version": version})


class PropertyImageViewSet(viewsets.ModelViewSet):
    queryset = PropertyImage.objects.select_related("property").all()
    serializer_class = PropertyImageSerializer
    permission_classes = [AllowAny]