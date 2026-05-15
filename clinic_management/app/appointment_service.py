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
from dataclasses import asdict, dataclass
from datetime import date
from typing import Optional

from django.db import transaction
from django.utils import timezone

from .decorators import log_execution, require_role
from .slot_engine import BookingResult, SlotEngine

logger = logging.getLogger("mediflow.appointment_service")

@dataclass
class AppointmentDTO:
    """Dữ liệu lịch hẹn được serialize trả về client."""
    id:              str
    patient_name:    str
    doctor_name:     str
    specialty:       str
    clinic_name:     str
    slot_date:       str          # ISO date string
    start_time:      str          # HH:MM
    end_time:        str          # HH:MM
    status:          str
    symptoms:        str
    consultation_fee: str
    booked_at:       str

    @classmethod
    def from_appointment(cls, apt) -> "AppointmentDTO":
        slot   = apt.slot
        doctor = apt.doctor
        return cls(
            id=str(apt.id),
            patient_name=apt.patient.user.full_name,
            doctor_name=doctor.user.full_name,
            specialty=doctor.get_specialty_display(),
            clinic_name=doctor.clinic.name if doctor.clinic else "",
            slot_date=str(slot.slot_date),
            start_time=slot.start_time.strftime("%H:%M"),
            end_time=slot.end_time.strftime("%H:%M"),
            status=apt.status,
            symptoms=apt.symptoms,
            consultation_fee=f"{doctor.consultation_fee:,.0f}đ",
            booked_at=apt.booked_at.strftime("%Y-%m-%d %H:%M"),
        )

    def to_dict(self) -> dict:
        return asdict(self)

class AppointmentService:

    def __init__(self):
        self._engine = SlotEngine()
        self._import_models()

    def _import_models(self):
        from .models import Appointment
        from .models import Patient
        self._Appointment = Appointment
        self._Patient = Patient


    @log_execution(level="INFO")
    def create(
        self,
        slot_id: str,
        patient,
        symptoms: str = "",
        note: str = "",
        user=None,
    ) -> tuple[bool, AppointmentDTO | str]:
        """
        Đặt lịch hẹn mới.

        Returns:
            (True,  AppointmentDTO) nếu thành công.
            (False, error_message)  nếu thất bại.
        """
        result: BookingResult = self._engine.book_slot(
            slot_id=slot_id,
            patient=patient,
            symptoms=symptoms,
            note=note,
            user=user,
        )

        if not result.success:
            logger.warning("create appointment failed: %s", result.error)
            return False, result.error

        # Lấy full object để build DTO
        apt = (
            self._Appointment.objects
            .select_related(
                "patient__user",
                "doctor__user",
                "doctor__clinic",
                "slot",
            )
            .get(pk=result.appointment_id)
        )

        # Gửi email xác nhận (async — không block response)
        self._send_confirmation_async(apt)

        return True, AppointmentDTO.from_appointment(apt)


    @log_execution(level="INFO")
    @require_role("doctor", "admin")
    def confirm(self, appointment_id: str, user=None) -> tuple[bool, AppointmentDTO | str]:
        """
        Bác sĩ / admin xác nhận lịch hẹn.

        Returns:
            (True,  AppointmentDTO) nếu xác nhận OK.
            (False, error_message)  nếu lịch hẹn không hợp lệ.
        """
        try:
            apt = (
                self._Appointment.objects
                .select_related(
                    "patient__user",
                    "doctor__user",
                    "doctor__clinic",
                    "slot",
                )
                .get(pk=appointment_id)
            )
        except self._Appointment.DoesNotExist:
            return False, f"Lịch hẹn {appointment_id} không tồn tại."

        if apt.status != "pending":
            return False, f"Lịch hẹn đang ở trạng thái '{apt.status}', không thể xác nhận."

        # Kiểm tra doctor chỉ xác nhận lịch của chính mình
        if hasattr(user, "doctor_profile"):
            if str(apt.doctor_id) != str(user.doctor_profile.id):
                return False, "Bạn chỉ có thể xác nhận lịch hẹn của chính mình."

        apt.confirm()

        # Gửi reminder cho bệnh nhân (Celery)
        self._send_reminder_async(apt)

        logger.info("confirm appointment=%s by user=%s", appointment_id, user)
        return True, AppointmentDTO.from_appointment(apt)


    @log_execution(level="INFO")
    def cancel(
        self,
        appointment_id: str,
        reason: str = "",
        user=None,
    ) -> tuple[bool, str]:
        """
        Huỷ lịch hẹn. Ai cũng có thể huỷ (patient / doctor / admin)
        nhưng patient bị giới hạn 2 giờ — xử lý trong SlotEngine.

        Returns:
            (True,  "Đã huỷ lịch hẹn thành công.")
            (False, error_message)
        """
        try:
            apt = (
                self._Appointment.objects
                .select_related("slot__schedule__doctor", "patient__user")
                .get(pk=appointment_id)
            )
        except self._Appointment.DoesNotExist:
            return False, f"Lịch hẹn {appointment_id} không tồn tại."

        if apt.status in ("cancelled", "completed"):
            return False, f"Lịch hẹn đã ở trạng thái '{apt.status}', không thể huỷ."

        try:
            self._engine.release_slot(appointment=apt, reason=reason, user=user)
        except PermissionError as e:
            return False, str(e)
        except Exception as e:
            logger.exception("cancel appointment=%s error: %s", appointment_id, e)
            return False, "Lỗi hệ thống khi huỷ lịch. Vui lòng thử lại."

        # Gửi thông báo huỷ (Celery)
        self._send_cancellation_async(apt, reason)

        return True, "Đã huỷ lịch hẹn thành công."

    def get_patient_appointments(
        self,
        patient_id: str,
        status: Optional[str] = None,
        from_date: Optional[date] = None,
    ) -> list[AppointmentDTO]:
        """
        Lấy danh sách lịch hẹn của patient với select_related tối ưu.
        Tránh N+1 query — dùng cho list view.
        """
        qs = (
            self._Appointment.objects
            .filter(patient_id=patient_id)
            .select_related(
                "patient__user",
                "doctor__user",
                "doctor__clinic",
                "slot",
            )
            .order_by("-slot__slot_date", "-slot__start_time")
        )

        if status:
            qs = qs.filter(status=status)
        if from_date:
            qs = qs.filter(slot__slot_date__gte=from_date)

        return [AppointmentDTO.from_appointment(apt) for apt in qs]

    def get_doctor_schedule(
        self,
        doctor_id: str,
        on_date: date,
    ) -> list[AppointmentDTO]:
        """
        Lịch làm việc của bác sĩ trong ngày — dùng cho doctor dashboard.
        prefetch_related để load medical_record nếu có.
        """
        qs = (
            self._Appointment.objects
            .filter(
                doctor_id=doctor_id,
                slot__slot_date=on_date,
            )
            .exclude(status="cancelled")
            .select_related(
                "patient__user",
                "doctor__user",
                "doctor__clinic",
                "slot",
            )
            .prefetch_related("medical_record")
            .order_by("slot__start_time")
        )

        return [AppointmentDTO.from_appointment(apt) for apt in qs]

    # ── ASYNC NOTIFICATIONS (Celery) ─────────────────────────

    @staticmethod
    def _send_confirmation_async(apt) -> None:
        """Gửi email xác nhận đặt lịch — không block."""
        try:
            from apps.notifications.tasks import send_booking_confirmation
            send_booking_confirmation.delay(str(apt.id))
        except Exception as e:
            logger.warning("Failed to queue confirmation email: %s", e)

    @staticmethod
    def _send_reminder_async(apt) -> None:
        """Lên lịch gửi reminder 24h trước giờ hẹn."""
        from datetime import datetime
        try:
            from apps.notifications.tasks import send_appointment_reminder
            from django.utils import timezone as tz
            slot_dt = datetime.combine(apt.slot.slot_date, apt.slot.start_time)
            remind_at = tz.make_aware(slot_dt) - timezone.timedelta(hours=24)
            send_appointment_reminder.apply_async(
                args=[str(apt.id)],
                eta=remind_at,
            )
        except Exception as e:
            logger.warning("Failed to queue reminder: %s", e)

    @staticmethod
    def _send_cancellation_async(apt, reason: str) -> None:
        """Gửi thông báo huỷ lịch."""
        try:
            from apps.notifications.tasks import send_cancellation_notice
            send_cancellation_notice.delay(str(apt.id), reason)
        except Exception as e:
            logger.warning("Failed to queue cancellation notice: %s", e)