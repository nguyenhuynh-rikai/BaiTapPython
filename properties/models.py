from __future__ import annotations
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Ward(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="wards")

    class Meta:
        unique_together = ("name", "district")

    def __str__(self):
        return f"{self.name}, {self.district.name}"


class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Property(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    area = models.FloatField()
    price_per_m2 = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)

    address = models.CharField(max_length=255, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    amenities = models.ManyToManyField(Amenity, blank=True)

    source_url = models.URLField(max_length=500, unique=True)
    source_name = models.CharField(max_length=50)
    posted_at_text = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["price", "area"]),
            models.Index(fields=["source_name"]),
            models.Index(fields=["is_active"]),
        ]

    # Type hints for dynamic reverse relationships (to satisfy static analysis/Pyrefly)
    images: models.Manager[PropertyImage]
    manager: PropertyManager
    appointments: models.Manager[ViewingAppointment]
    in_comparisons: models.Manager[ComparisonList]

    def __str__(self):
        return self.title


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="images")
    image_url = models.URLField(max_length=500)

    def __str__(self):
        return self.image_url


class FavoriteProperty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "property")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.property.title}"


class PropertyManager(models.Model):
    """
    Bảng mapping để gán quyền sở hữu phòng (Chủ trọ - Landlord) mà không sửa bảng Property.
    """
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name="manager")
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name="managed_properties")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["landlord"]),
        ]

    def __str__(self):
        return f"{self.landlord.username} quản lý {self.property.title}"


class ViewingAppointment(models.Model):
    """
    Bảng quản lý lịch hẹn xem phòng của Guest với Landlord.
    """
    STATUS_CHOICES = (
        ("PENDING", "Chờ xác nhận"),
        ("CONFIRMED", "Đã xác nhận"),
        ("CANCELLED", "Đã hủy"),
        ("COMPLETED", "Đã hoàn thành"),
    )
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="appointments")
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name="guest_appointments")
    # Lưu trực tiếp landlord ở đây để tối ưu hóa việc truy vấn danh sách lịch hẹn của landlord
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name="landlord_appointments")
    
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    note = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-appointment_date"]
        indexes = [
            models.Index(fields=["guest", "status"]),
            models.Index(fields=["landlord", "status"]),
            models.Index(fields=["appointment_date"]),
        ]

    def __str__(self):
        return f"Lịch hẹn {self.guest.username} xem {self.property.title} lúc {self.appointment_date}"


class ComparisonList(models.Model):
    """
    Bảng lưu danh sách phòng đang so sánh của User.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="comparison_list")
    properties = models.ManyToManyField(Property, related_name="in_comparisons")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Danh sách so sánh của {self.user.username}"


