from django.db.models import Avg, Count, Min, Max
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Amenity, Category, District, Property, PropertyImage, Ward
from .serializers import (
    AmenitySerializer,
    CategorySerializer,
    DistrictSerializer,
    PropertyImageSerializer,
    PropertySerializer,
    WardSerializer,
)


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
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description", "address", "district__name", "ward__name"]
    ordering_fields = ["price", "area", "price_per_m2", "created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = (
            Property.objects.select_related("category", "district", "ward")
            .prefetch_related("amenities", "images")
            .all()
        )

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

        return queryset

    @action(detail=False, methods=["get"])
    def stats(self, request):
        queryset = self.get_queryset()
        data = queryset.aggregate(
            total=Count("id"),
            min_price=Min("price"),
            max_price=Max("price"),
            avg_price=Avg("price"),
            min_area=Min("area"),
            max_area=Max("area"),
            avg_area=Avg("area"),
        )

        return Response(data)


class PropertyImageViewSet(viewsets.ModelViewSet):
    queryset = PropertyImage.objects.select_related("property").all()
    serializer_class = PropertyImageSerializer
    permission_classes = [AllowAny]
