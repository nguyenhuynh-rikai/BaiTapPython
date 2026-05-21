from rest_framework import permissions

class IsAppointmentParticipant(permissions.BasePermission):
    """
    Quyền truy cập dành riêng cho người tham gia lịch hẹn (Khách thuê hoặc Chủ trọ).
    Admin hệ thống cũng được phép truy cập để quản lý.
    """
    def has_permission(self, request, view):
        # Người dùng phải đăng nhập trước
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Admin luôn có quyền tối cao
        if getattr(request.user, "is_staff", False):
            return True
        # Chỉ Guest đặt lịch hoặc Landlord của lịch hẹn mới được xem/chỉnh sửa
        return obj.guest == request.user or obj.landlord == request.user
