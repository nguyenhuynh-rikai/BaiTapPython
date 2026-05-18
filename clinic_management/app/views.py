"""
MediFlow — api/views.py
=========================
ViewSets + APIViews cho toàn bộ hệ thống.

Endpoints được đăng ký (xem urls.py):
  /api/auth/register/
  /api/auth/login/
  /api/auth/token/refresh/
  /api/auth/me/
  /api/auth/change-password/

  /api/clinics/                          (CRUD - admin only write)
  /api/doctors/                          (list, retrieve)
  /api/doctors/{id}/workload/            (admin/doctor)
  /api/doctors/{id}/schedule/            (lịch ngày của bác sĩ)

  /api/patients/me/                      (hồ sơ bản thân)
  /api/patients/{id}/appointments/       (lịch sử khám)

  /api/slots/available/                  (GET - xem slot trống)

  /api/appointments/                     (POST - đặt lịch)
  /api/appointments/{id}/                (GET, DELETE)
  /api/appointments/{id}/confirm/        (PATCH - bác sĩ/admin xác nhận)
  /api/appointments/{id}/medical-record/ (GET, POST)

  /api/drugs/                            (list, retrieve - full-text search)
  /api/payments/{id}/                    (GET, PATCH status)
"""

import logging
from datetime import date

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.utils import timezone
from rest_framework import filters, generics, mixins, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework_simplejwt.views import TokenRefreshView

from .models import Appointment
from .permissions import (
    IsAdmin, IsAppointmentParticipant, IsDoctorOrAdmin,
    IsOwnerOrAdmin, IsPatient, ReadOnlyOrAdmin,
)
from .serializers import (
    AppointmentCancelSerializer, AppointmentCreateSerializer,
    AppointmentDetailSerializer, AppointmentListSerializer,
    AvailableSlotsQuerySerializer, ChangePasswordSerializer,
    ClinicSerializer, DoctorDetailSerializer, DoctorListSerializer,
    DoctorWorkloadSerializer, DrugSerializer, LoginSerializer,
    MedicalRecordCreateSerializer, MedicalRecordSerializer,
    PatientSerializer, PatientUpdateSerializer, PaymentSerializer,
    RegisterSerializer, TimeSlotSerializer, UserMeSerializer,
    WorkloadQuerySerializer,
)
from .appointment_service import AppointmentService
from .slot_engine import SlotEngine

logger = logging.getLogger("mediflow.api")


# ─────────────────────────────────────────────────────────────
# PAGINATION
# ─────────────────────────────────────────────────────────────

class StandardPagination(PageNumberPagination):
    page_size              = 20
    page_size_query_param  = "page_size"
    max_page_size          = 100

    def get_paginated_response(self, data):
        return Response({
            "count":    self.page.paginator.count,
            "total_pages": self.page.paginator.num_pages,
            "next":     self.get_next_link(),
            "previous": self.get_previous_link(),
            "results":  data,
        })

class RegisterView(generics.CreateAPIView):
    """
    POST /auth/register/
    Đăng ký tài khoản mới. Không cần xác thực.
    """
    permission_classes = [AllowAny]
    serializer_class   = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        logger.info("New user registered: %s (role=%s)", user.email, user.role)
        return Response(
            {"message": "Đăng ký thành công. Vui lòng kiểm tra email để xác nhận tài khoản."},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """
    POST /auth/login/
    Trả về JWT access + refresh token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        logger.info("Login: %s", request.data.get("email", ""))
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class MeView(generics.RetrieveUpdateAPIView):
    """
    GET  /auth/me/  — xem thông tin bản thân
    PATCH /auth/me/ — cập nhật full_name, phone
    """
    permission_classes = [IsAuthenticated]
    serializer_class   = UserMeSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    """
    POST /auth/change-password/
    Đổi mật khẩu — yêu cầu đăng nhập.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info("Password changed for user: %s", request.user.email)
        return Response({"message": "Đổi mật khẩu thành công."})


# ─────────────────────────────────────────────────────────────
# CLINIC VIEWSET
# ─────────────────────────────────────────────────────────────

class ClinicViewSet(ModelViewSet):
    """
    GET    /clinics/         — danh sách phòng khám
    POST   /clinics/         — tạo mới (admin)
    GET    /clinics/{id}/    — chi tiết
    PATCH  /clinics/{id}/    — cập nhật (admin)
    DELETE /clinics/{id}/    — xoá (admin)
    """
    serializer_class   = ClinicSerializer
    permission_classes = [ReadOnlyOrAdmin]
    pagination_class   = StandardPagination
    filter_backends    = [filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ["name", "address"]
    ordering_fields    = ["name", "created_at"]
    ordering           = ["name"]

    def get_queryset(self):
        from .models import Clinic
        qs = Clinic.objects.filter(is_active=True)
        return qs


# ─────────────────────────────────────────────────────────────
# DOCTOR VIEWSET
# ─────────────────────────────────────────────────────────────

class DoctorViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):

    permission_classes = [IsAuthenticated]
    pagination_class   = StandardPagination
    filter_backends    = [filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ["user__full_name", "specialty", "clinic__name"]
    ordering_fields    = ["experience_years", "consultation_fee"]
    ordering           = ["user__full_name"]

    def get_queryset(self):
        from .models import Doctor
        qs = (
            Doctor.objects
            .filter(user__is_active=True)
            .select_related("user", "clinic")
            .prefetch_related("work_schedules")
        )
        # Filter theo specialty nếu có
        specialty = self.request.query_params.get("specialty")
        if specialty:
            qs = qs.filter(specialty=specialty)
        # Filter chỉ nhận bệnh nhân mới
        accepting = self.request.query_params.get("accepting")
        if accepting == "true":
            qs = qs.filter(is_accepting_new=True)
        return qs

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DoctorDetailSerializer
        return DoctorListSerializer

    @action(
        detail=True,
        methods=["get"],
        url_path="workload",
        permission_classes=[IsDoctorOrAdmin],
    )
    def workload(self, request, pk=None):
        """GET /api/doctors/{id}/workload/?from_date=&to_date="""
        # Doctor chỉ xem được workload của chính mình
        if request.user.role == "doctor":
            if not hasattr(request.user, "doctor_profile"):
                return Response({"detail": "Không tìm thấy hồ sơ bác sĩ."}, status=404)
            if str(request.user.doctor_profile.id) != pk:
                return Response({"detail": "Bạn chỉ xem được thống kê của mình."}, status=403)

        query_ser = WorkloadQuerySerializer(data=request.query_params)
        query_ser.is_valid(raise_exception=True)

        engine   = SlotEngine()
        workload = engine.get_doctor_workload(
            doctor_id=pk,
            from_date=query_ser.validated_data["from_date"],
            to_date=query_ser.validated_data["to_date"],
        )
        return Response(DoctorWorkloadSerializer(workload).data)

    @action(
        detail=True,
        methods=["get"],
        url_path="schedule",
        permission_classes=[IsDoctorOrAdmin],
    )
    def schedule(self, request, pk=None):
        """GET /api/doctors/{id}/schedule/?date=YYYY-MM-DD"""
        raw_date = request.query_params.get("date")
        try:
            on_date = date.fromisoformat(raw_date) if raw_date else date.today()
        except ValueError:
            return Response({"detail": "Định dạng ngày không hợp lệ (YYYY-MM-DD)."}, status=400)

        service   = AppointmentService()
        schedules = service.get_doctor_schedule(doctor_id=pk, on_date=on_date)
        return Response([s.to_dict() for s in schedules])


# ─────────────────────────────────────────────────────────────
# PATIENT VIEWS
# ─────────────────────────────────────────────────────────────

class PatientMeView(generics.RetrieveUpdateAPIView):
    """
    GET   /patients/me/   — xem hồ sơ bản thân
    PATCH /patients/me/   — cập nhật hồ sơ
    """
    permission_classes = [IsPatient]

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return PatientUpdateSerializer
        return PatientSerializer

    def get_object(self):
        try:
            return self.request.user.patient_profile
        except Exception:
            from rest_framework.exceptions import NotFound
            raise NotFound("Không tìm thấy hồ sơ bệnh nhân. Vui lòng liên hệ admin.")

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


class PatientAppointmentsView(generics.ListAPIView):
    """
    GET /patients/me/appointments/?status=&from_date=
    Lịch sử khám của bệnh nhân đang đăng nhập.
    """
    permission_classes = [IsPatient]
    serializer_class   = AppointmentListSerializer
    pagination_class   = StandardPagination

    def get_queryset(self):
        # Trả về list DTO — không phải queryset Django
        # Override list() để xử lý
        return []

    def list(self, request, *args, **kwargs):
        status_filter    = request.query_params.get("status")
        from_date_raw    = request.query_params.get("from_date")
        from_date        = None

        if from_date_raw:
            try:
                from_date = date.fromisoformat(from_date_raw)
            except ValueError:
                return Response({"detail": "Định dạng from_date không hợp lệ."}, status=400)

        service      = AppointmentService()
        patient      = request.user.patient_profile
        appointments = service.get_patient_appointments(
            patient_id=str(patient.id),
            status=status_filter,
            from_date=from_date,
        )

        # Paginate DTOs
        page = self.paginate_queryset(appointments)
        if page is not None:
            data = [apt.to_dict() for apt in page]
            return self.get_paginated_response(data)

        return Response([apt.to_dict() for apt in appointments])


# ─────────────────────────────────────────────────────────────
# SLOT VIEWS
# ─────────────────────────────────────────────────────────────

class AvailableSlotsView(APIView):
    """
    GET /slots/available/?doctor_id=&date=YYYY-MM-DD
    GET /slots/available/?specialty=cardiology&date=YYYY-MM-DD
    Trả danh sách slot trống. Cache 60 giây trong SlotEngine.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query_ser = AvailableSlotsQuerySerializer(data=request.query_params)
        query_ser.is_valid(raise_exception=True)

        engine = SlotEngine()
        slots  = engine.get_available_slots(
            doctor_id=str(query_ser.validated_data.get("doctor_id", "")),
            on_date=query_ser.validated_data["date"],
            specialty=query_ser.validated_data.get("specialty", ""),
        )
        return Response(TimeSlotSerializer(slots, many=True).data)


# ─────────────────────────────────────────────────────────────
# APPOINTMENT VIEWSET
# ─────────────────────────────────────────────────────────────

class AppointmentViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    POST   /appointments/              — đặt lịch (patient)
    GET    /appointments/{id}/         — chi tiết
    DELETE /appointments/{id}/         — huỷ lịch
    PATCH  /appointments/{id}/confirm/ — xác nhận (doctor/admin)
    GET    /appointments/{id}/medical-record/ — xem hồ sơ
    POST   /appointments/{id}/medical-record/ — tạo hồ sơ (doctor)
    """
    queryset = Appointment.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class   = StandardPagination

    def get_queryset(self):
        from .models import Appointment
        qs = (
            Appointment.objects
            .select_related(
                "patient__user",
                "doctor__user",
                "doctor__clinic",
                "slot",
            )
            .prefetch_related("medical_record")
        )
        user = self.request.user
        if user.role == "patient":
            return qs.filter(patient__user=user)
        if user.role == "doctor":
            return qs.filter(doctor__user=user)
        return qs

    def get_serializer_class(self):
        if self.action == "create":
            return AppointmentCreateSerializer
        if self.action == "destroy":
            return AppointmentCancelSerializer
        return AppointmentDetailSerializer

    def get_permissions(self):
        if self.action == "create":
            return [IsPatient()]
        if self.action == "confirm":
            return [IsDoctorOrAdmin()]
        return [IsAuthenticated(), IsAppointmentParticipant()]

    # ── POST /api/appointments/ ──────────────────────────────
    def create(self, request, *args, **kwargs):
        serializer = AppointmentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            patient = request.user.patient_profile
        except Exception:
            return Response(
                {"detail": "Không tìm thấy hồ sơ bệnh nhân."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        service    = AppointmentService()
        ok, result = service.create(
            slot_id=serializer.validated_data["slot_id"],
            patient=patient,
            symptoms=serializer.validated_data.get("symptoms", ""),
            note=serializer.validated_data.get("note", ""),
            user=request.user,
        )

        if not ok:
            return Response({"detail": result}, status=status.HTTP_400_BAD_REQUEST)

        logger.info("Appointment created: %s by patient %s", result.id, patient.id)
        return Response(result.to_dict(), status=status.HTTP_201_CREATED)

    # ── DELETE /api/appointments/{id}/ ──────────────────────
    def destroy(self, request, *args, **kwargs):
        appointment = self.get_object()
        reason      = request.data.get("reason", "")

        service    = AppointmentService()
        ok, message = service.cancel(
            appointment_id=str(appointment.id),
            reason=reason,
            user=request.user,
        )

        if not ok:
            return Response({"detail": message}, status=status.HTTP_400_BAD_REQUEST)

        logger.info("Appointment cancelled: %s by user %s", appointment.id, request.user.id)
        return Response({"detail": message}, status=status.HTTP_200_OK)

    # ── PATCH /api/appointments/{id}/confirm/ ───────────────
    @action(detail=True, methods=["patch"], url_path="confirm")
    def confirm(self, request, pk=None):
        service    = AppointmentService()
        ok, result = service.confirm(
            appointment_id=pk,
            user=request.user,
        )

        if not ok:
            return Response({"detail": result}, status=status.HTTP_400_BAD_REQUEST)

        logger.info("Appointment confirmed: %s by %s", pk, request.user.email)
        return Response(result.to_dict())

    # ── GET/POST /api/appointments/{id}/medical-record/ ─────
    @action(detail=True, methods=["get", "post"], url_path="medical-record")
    def medical_record(self, request, pk=None):
        from .models import MedicalRecord
        appointment = self.get_object()

        if request.method == "GET":
            try:
                record     = appointment.medical_record
                serializer = MedicalRecordSerializer(record)
                return Response(serializer.data)
            except MedicalRecord.DoesNotExist:
                return Response(
                    {"detail": "Chưa có hồ sơ khám cho lịch hẹn này."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        # POST — chỉ doctor của lịch hẹn này
        if request.user.role != "doctor":
            return Response(
                {"detail": "Chỉ bác sĩ mới có thể tạo hồ sơ khám."},
                status=status.HTTP_403_FORBIDDEN,
            )
        if appointment.doctor.user_id != request.user.id:
            return Response(
                {"detail": "Bạn không phải bác sĩ của lịch hẹn này."},
                status=status.HTTP_403_FORBIDDEN,
            )
        if appointment.status != "confirmed":
            return Response(
                {"detail": "Chỉ tạo hồ sơ cho lịch hẹn đã được xác nhận."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = MedicalRecordCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        record = serializer.save(appointment=appointment)

        # Đánh dấu appointment là completed
        appointment.status = "completed"
        appointment.save(update_fields=["status", "updated_at"])

        logger.info("Medical record created for appointment %s", pk)
        return Response(
            MedicalRecordSerializer(record).data,
            status=status.HTTP_201_CREATED,
        )


# ─────────────────────────────────────────────────────────────
# DRUG VIEWSET
# ─────────────────────────────────────────────────────────────
class DrugViewSet(ReadOnlyModelViewSet):

    serializer_class   = DrugSerializer
    permission_classes = [IsAuthenticated]
    pagination_class   = StandardPagination

    def get_queryset(self):

        from .models import Drug

        qs = Drug.objects.filter(is_active=True)

        query = self.request.query_params.get("search")

        if query:
            vector = (
                SearchVector("name", weight="A") +
                SearchVector("generic_name", weight="A") +
                SearchVector("description", weight="B")
            )

            search_query = SearchQuery(query)

            qs = (
                qs.annotate(
                    rank=SearchRank(vector, search_query)
                )
                .filter(rank__gte=0.1)
                .order_by("-rank")
            )

        return qs
# ─────────────────────────────────────────────────────────────
# PAYMENT VIEW
# ─────────────────────────────────────────────────────────────

class PaymentDetailView(generics.RetrieveUpdateAPIView):
    """
    GET   /payments/{id}/  — xem thông tin thanh toán
    PATCH /payments/{id}/  — cập nhật trạng thái (admin)
    """
    serializer_class   = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        from .models import Payment
        qs = Payment.objects.select_related("appointment__patient__user")
        user = self.request.user
        if user.role == "admin":
            return qs
        if user.role == "patient":
            return qs.filter(appointment__patient__user=user)
        return qs.none()

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH"):
            return [IsAdmin()]
        return [IsAuthenticated()]
