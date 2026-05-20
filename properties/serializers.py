from rest_framework import serializers

from .models import Amenity, Category, District, FavoriteProperty, Property, PropertyImage, Ward


class CategorySerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore
        model = Category
        fields = ["id", "name", "slug"]


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore
        model = District
        fields = ["id", "name"]


class WardSerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(source="district.name", read_only=True)

    class Meta:  # type: ignore
        model = Ward
        fields = ["id", "name", "district", "district_name"]


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore
        model = Amenity
        fields = ["id", "name", "icon"]


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore
        model = PropertyImage
        fields = ["id", "property", "image_url"]


class PropertySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    district_name = serializers.CharField(source="district.name", read_only=True)
    ward_name = serializers.CharField(source="ward.name", read_only=True)
    amenities_detail = AmenitySerializer(source="amenities", many=True, read_only=True)
    images = PropertyImageSerializer(many=True, read_only=True)

    class Meta:  # type: ignore
        model = Property
        fields = [
            "id",
            "title",
            "description",
            "price",
            "area",
            "price_per_m2",
            "address",
            "district",
            "district_name",
            "ward",
            "ward_name",
            "latitude",
            "longitude",
            "category",
            "category_name",
            "amenities",
            "amenities_detail",
            "source_url",
            "source_name",
            "posted_at_text",
            "images",
            "is_active",
            "created_at",
            "updated_at",
        ]


class ImportPropertiesSerializer(serializers.Serializer):
    csv_path = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Đường dẫn đến file CSV để import (mặc định: data/rooms_cleaned.csv)"
    )


class FavoritePropertySerializer(serializers.ModelSerializer):
    property_detail = PropertySerializer(source="property", read_only=True)

    class Meta:  # type: ignore
        model = FavoriteProperty
        fields = ["id", "property", "property_detail", "created_at"]
        read_only_fields = ["id", "created_at"]

