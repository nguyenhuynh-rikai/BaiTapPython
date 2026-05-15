"""
MediFlow — api/permissions.py
================================
Custom DRF Permission classes theo role.

  IsPatient        — chỉ bệnh nhân
  IsDoctor         — chỉ bác sĩ
  IsAdmin          — chỉ admin
  IsDoctorOrAdmin  — bác sĩ hoặc admin
  IsOwnerOrAdmin   — chủ sở hữu object hoặc admin
  IsAppointmentParticipant — patient/doctor của lịch hẹn đó, hoặc admin
"""

from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


class IsPatient(IsAuthenticated):
    """Chỉ cho phép user có role=patient."""
    message = "Chỉ bệnh nhân mới có quyền thực hiện thao tác này."

    def has_permission(self, request, view) -> bool:
        return (
            super().has_permission(request, view)
            and request.user.role == "patient"
        )


class IsDoctor(IsAuthenticated):
    """Chỉ cho phép user có role=doctor."""
    message = "Chỉ bác sĩ mới có quyền thực hiện thao tác này."

    def has_permission(self, request, view) -> bool:
        return (
            super().has_permission(request, view)
            and request.user.role == "doctor"
        )


class IsAdmin(IsAuthenticated):
    """Chỉ cho phép admin."""
    message = "Chỉ quản trị viên mới có quyền thực hiện thao tác này."

    def has_permission(self, request, view) -> bool:
        return (
            super().has_permission(request, view)
            and request.user.role == "admin"
        )


class IsDoctorOrAdmin(IsAuthenticated):
    """Bác sĩ hoặc admin."""
    message = "Yêu cầu quyền bác sĩ hoặc quản trị viên."

    def has_permission(self, request, view) -> bool:
        return (
            super().has_permission(request, view)
            and request.user.role in ("doctor", "admin")
        )


class IsOwnerOrAdmin(IsAuthenticated):
    """
    Object-level: user phải là chủ sở hữu (obj.user == request.user)
    hoặc là admin.

    Object phải có thuộc tính `user` (ForeignKey / OneToOne đến User).
    """
    message = "Bạn không có quyền truy cập tài nguyên này."

    def has_object_permission(self, request, view, obj) -> bool:
        if request.user.role == "admin":
            return True
        # obj có thể là Patient/Doctor (có .user) hoặc chính là User
        owner = getattr(obj, "user", obj)
        return owner == request.user


class IsAppointmentParticipant(IsAuthenticated):
    """
    Object-level cho Appointment:
    - patient của lịch hẹn
    - doctor của lịch hẹn
    - admin
    có thể xem; chỉ patient mới đặt, chỉ doctor/admin mới confirm.
    """
    message = "Bạn không phải bệnh nhân hoặc bác sĩ của lịch hẹn này."

    def has_object_permission(self, request, view, obj) -> bool:
        user = request.user
        if user.role == "admin":
            return True
        if user.role == "patient":
            return obj.patient.user_id == user.id
        if user.role == "doctor":
            return obj.doctor.user_id == user.id
        return False


class ReadOnlyOrAdmin(IsAuthenticated):
    """
    GET/HEAD/OPTIONS: mọi user đã đăng nhập.
    POST/PUT/PATCH/DELETE: chỉ admin.
    """
    message = "Chỉ quản trị viên mới có thể thay đổi dữ liệu này."

    def has_permission(self, request, view) -> bool:
        if not super().has_permission(request, view):
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.role == "admin"
