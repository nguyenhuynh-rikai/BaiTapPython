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


from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.contrib.auth.models import Group
from django.http import HttpRequest
from typing import Any
from django.contrib.auth.forms import UserChangeForm

# Định nghĩa Form chỉnh sửa người dùng tùy biến hỗ trợ chọn Vai Trò
class UserAdminForm(UserChangeForm):
    first_name = forms.CharField(label='Họ và tên', required=False)
    role = forms.ChoiceField(
        choices=[
            ('tenant', 'Khách Thuê Phòng (Tenant)'),
            ('landlord', 'Chủ Cho Thuê (Landlord)'),
            ('admin', 'Quản Trị Viên (Admin)')
        ],
        label='Phân quyền: ',
        required=True
    )

    class Meta(UserChangeForm.Meta):
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Gán giá trị ban đầu (initial) dựa trên group hoặc trạng thái admin
            if self.instance.is_superuser or self.instance.is_staff:
                self.initial['role'] = 'admin'
            elif self.instance.groups.filter(name='landlord').exists():
                self.initial['role'] = 'landlord'
            else:
                self.initial['role'] = 'tenant'

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')
        
        # Đồng bộ trạng thái staff/superuser trực tiếp trên đối tượng user
        if role == 'admin':
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = False
            user.is_superuser = False
            
        if commit:
            user.save()
            
        return user

admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    form = UserAdminForm
    
    # Ghi đè save_related để đảm bảo đồng bộ group sau khi Django Admin lưu xong các quan hệ Many-to-Many mặc định
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        role = form.cleaned_data.get('role')
        if role:
            user = form.instance
            user.groups.clear()
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)
    
    # Những cột hiển thị ở danh sách ngoài (List View)
    list_display = ('username', 'get_role', 'get_full_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    
    @admin.display(description='Họ và Tên')
    def get_full_name(self, obj):
        return obj.first_name if obj.first_name else "-"
    
    @admin.display(description='Vai Trò (Role)')
    def get_role(self, obj):
        if obj.is_superuser or obj.is_staff:
            return "Admin"
        elif obj.groups.filter(name="landlord").exists():
            return "Chủ Cho Thuê (Landlord)"
        elif obj.groups.filter(name="tenant").exists():
            return "Khách Thuê (Tenant)"
        return "Khách Thuê (Tenant)" # Mặc định

    # Can thiệp form chi tiết: Ẩn email và Thêm hộp chọn Vai Trò vào nhóm đầu tiên
    def get_fieldsets(self, request: HttpRequest, obj: "Any" = None) -> "Any":
        if not obj:
            return super().get_fieldsets(request, obj)
            
        fieldsets = list(super().get_fieldsets(request, obj))
        new_fieldsets = []
        for i, (title, info) in enumerate(fieldsets):
            fields = list(info.get('fields', []))
            
            # Xóa trường email và last_name khỏi giao diện để tránh rườm rà
            if 'email' in fields:
                fields.remove('email')
            if 'last_name' in fields:
                fields.remove('last_name')
                
            # Chèn trường role động vào chung nhóm thông tin đăng nhập đầu tiên
            if i == 0:
                fields.append('role')
                
            new_fieldsets.append((title, {**info, 'fields': fields}))
        return tuple(new_fieldsets)