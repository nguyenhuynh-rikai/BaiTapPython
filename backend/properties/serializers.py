from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone

from .models import (
    Amenity, Category, ComparisonList, District, FavoriteProperty, Property, 
    PropertyImage, PropertyManager, ViewingAppointment, Ward
)



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
            "status",
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


class ViewingAppointmentSerializer(serializers.ModelSerializer):
    property_detail = PropertySerializer(source="property", read_only=True)
    guest_username = serializers.CharField(source="guest.username", read_only=True)
    landlord_username = serializers.CharField(source="landlord.username", read_only=True)

    class Meta:  # type: ignore
        model = ViewingAppointment
        fields = [
            "id",
            "property",
            "property_detail",
            "guest",
            "guest_username",
            "landlord",
            "landlord_username",
            "appointment_date",
            "status",
            "note",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["guest", "landlord", "created_at", "updated_at"]

    def validate_appointment_date(self, value):
        # Đảm bảo ngày hẹn phải ở tương lai
        if value <= timezone.now():
            raise serializers.ValidationError("Thời gian hẹn xem phòng phải ở tương lai.")
        return value

    def validate(self, attrs):
        request = self.context.get("request")
        if not request or not request.user:
            raise serializers.ValidationError("Yêu cầu cần phải được xác thực.")

        property_obj = attrs.get("property")
        if property_obj:
            # Đảm bảo phòng trọ này đã được gán cho một chủ trọ quản lý
            # Dùng try/except vì hasattr trên reverse OneToOne luôn trả True
            try:
                _ = property_obj.manager
            except Exception:
                raise serializers.ValidationError(
                    "Phòng trọ này hiện chưa được gán cho chủ trọ nào quản lý. Không thể đặt lịch."
                )

            landlord = property_obj.manager.landlord

            # Guest không được tự đặt lịch xem phòng của mình (nếu guest chính là landlord)
            if request.user == landlord:
                raise serializers.ValidationError("Chủ trọ không thể tự đặt lịch hẹn xem phòng của chính mình.")

        return attrs


class ComparisonListSerializer(serializers.ModelSerializer):
    properties_detail = PropertySerializer(source="properties", many=True, read_only=True)

    class Meta:  # type: ignore
        model = ComparisonList
        fields = ["id", "user", "properties", "properties_detail", "updated_at"]
        read_only_fields = ["user", "updated_at"]


