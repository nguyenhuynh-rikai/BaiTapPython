from django.contrib import admin
from .models import Category, District, Ward, Amenity, Property, PropertyImage, PropertyManager, ViewingAppointment

# 1. Hiển thị ảnh ngay bên trong bài đăng phòng trọ (Inline)
class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1 # Cho phép thêm nhanh 1 ảnh mới

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    # Những cột sẽ hiển thị ở danh sách ngoài
    list_display = ('title', 'price', 'area', 'ward', 'district', 'source_name', 'is_active', 'created_at')

    # Bộ lọc ở cột bên phải
    list_filter = ('is_active', 'source_name', 'category', 'district')

    # Ô tìm kiếm
    search_fields = ('title', 'description', 'address')

    # Tích hợp quản lý ảnh vào chung một trang
    inlines = [PropertyImageInline]

    # Sắp xếp mặc định
    ordering = ('-created_at',)

# 2. Đăng ký các bảng còn lại đơn giản
admin.site.register(Category)
admin.site.register(District)
admin.site.register(Ward)
admin.site.register(Amenity)
admin.site.register(ViewingAppointment)

@admin.register(PropertyManager)
class PropertyManagerAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'landlord', 'created_at')
    raw_id_fields = ('property', 'landlord')
    search_fields = ('property__title', 'landlord__username')