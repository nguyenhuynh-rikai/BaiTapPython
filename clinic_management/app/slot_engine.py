"""
MediFlow — core/slot_engine.py
================================
SlotEngine: class OOP xử lý toàn bộ logic lịch hẹn.

Trách nhiệm:
  1. generate_slots()        — sinh TimeSlot từ WorkSchedule cho 1 tuần
  2. get_available_slots()   — trả danh sách slot trống theo doctor + ngày
  3. book_slot()             — đặt slot (atomic, chống race condition)
  4. release_slot()          — trả slot về trống khi huỷ lịch
  5. check_conflict()        — kiểm tra xung đột trước khi book
  6. get_doctor_workload()   — thống kê tỷ lệ đặt lịch của bác sĩ
"""

import logging
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from typing import Optional

from django.db import transaction
from django.utils import timezone

from .decorators import audit_action, cache_result, log_execution, require_role

logger = logging.getLogger("mediflow.slot_engine")

@dataclass
class SlotInfo:
    """Thông tin một slot trả về cho API / UI."""
    slot_id:    str
    doctor_id:  str
    date:       date
    start_time: time
    end_time:   time
    is_booked:  bool
    doctor_name: str = ""
    specialty:   str = ""

    @property
    def display(self) -> str:
        return f"{self.date} {self.start_time:%H:%M}–{self.end_time:%H:%M}"


@dataclass
class BookingResult:
    """Kết quả sau khi đặt lịch."""
    success:        bool
    appointment_id: Optional[str] = None
    slot:           Optional[SlotInfo] = None
    error:          str = ""


@dataclass
class DoctorWorkload:
    """Thống kê workload bác sĩ trong khoảng thời gian."""
    doctor_id:      str
    doctor_name:    str
    total_slots:    int
    booked_slots:   int
    completed:      int
    cancelled:      int
    no_show:        int
    utilization_pct: float = field(init=False)

    def __post_init__(self):
        self.utilization_pct = (
            round(self.booked_slots / self.total_slots * 100, 1)
            if self.total_slots else 0.0
        )

class SlotNotAvailableError(Exception):
    """Slot đã bị đặt hoặc không tồn tại."""

class SlotConflictError(Exception):
    """Patient đã có lịch hẹn trùng giờ."""

class ScheduleNotFoundError(Exception):
    """Bác sĩ không có lịch làm việc vào ngày yêu cầu."""


class SlotEngine:


    # Số ngày tối đa có thể đặt lịch trước
    MAX_ADVANCE_DAYS: int = 60
    # Thời gian tối thiểu trước giờ hẹn (phút) để có thể đặt
    MIN_LEAD_TIME_MINUTES: int = 30

    def __init__(self):
        # Import lazy — tránh circular import, dễ mock khi test
        from .models import Appointment, TimeSlot, WorkSchedule
        from .models import Doctor, Patient

        self._WorkSchedule  = WorkSchedule
        self._TimeSlot      = TimeSlot
        self._Appointment   = Appointment
        self._Doctor        = Doctor
        self._Patient       = Patient


    @log_execution(level="INFO")
    def generate_slots(self, doctor_id: str, from_date: date, to_date: date) -> int:
        """
        Sinh TimeSlot cho doctor trong khoảng [from_date, to_date].
        Được gọi bởi Celery task hàng tuần.

        Returns:
            Số slot mới được tạo.
        """
        schedules = (
            self._WorkSchedule.objects
            .filter(doctor_id=doctor_id, is_active=True)
            .select_related("doctor__user")
        )

        if not schedules.exists():
            raise ScheduleNotFoundError(
                f"Bác sĩ {doctor_id} chưa có lịch làm việc nào được cấu hình."
            )

        created_count = 0
        current = from_date

        while current <= to_date:
            weekday = current.weekday()          # 0=Mon … 6=Sun
            day_schedules = [s for s in schedules if s.weekday == weekday]

            for schedule in day_schedules:
                slots = self._split_into_slots(schedule, current)
                for slot_start, slot_end in slots:
                    _, created = self._TimeSlot.objects.get_or_create(
                        schedule=schedule,
                        slot_date=current,
                        start_time=slot_start,
                        defaults={"end_time": slot_end, "is_booked": False},
                    )
                    if created:
                        created_count += 1

            current += timedelta(days=1)

        logger.info(
            "generate_slots: doctor=%s  %s→%s  created=%d",
            doctor_id, from_date, to_date, created_count,
        )
        return created_count

    def _split_into_slots(
        self, schedule, on_date: date
    ) -> list[tuple[time, time]]:
        """Chia ca làm việc thành các slot nhỏ theo slot_duration_min."""
        slots = []
        duration = timedelta(minutes=schedule.slot_duration_min)

        current_dt = datetime.combine(on_date, schedule.start_time)
        end_dt     = datetime.combine(on_date, schedule.end_time)

        while current_dt + duration <= end_dt:
            slots.append((current_dt.time(), (current_dt + duration).time()))
            current_dt += duration

        return slots


    @cache_result(ttl=60, key_prefix="available_slots")
    @log_execution
    def get_available_slots(
        self,
        doctor_id: str,
        on_date: date,
        specialty: str = "",
    ) -> list[SlotInfo]:
      
        now = timezone.now()

        qs = (
            self._TimeSlot.objects
            .filter(slot_date=on_date, is_booked=False)
            .select_related("schedule__doctor__user", "schedule__doctor__clinic")
        )

        if doctor_id:
            qs = qs.filter(schedule__doctor_id=doctor_id)
        elif specialty:
            qs = qs.filter(schedule__doctor__specialty=specialty)

        result = []
        for slot in qs.order_by("start_time"):
            # Bỏ qua slot quá gần hiện tại
            slot_dt = datetime.combine(slot.slot_date, slot.start_time)
            slot_dt = timezone.make_aware(slot_dt) if timezone.is_naive(slot_dt) else slot_dt
            if (slot_dt - now).total_seconds() < self.MIN_LEAD_TIME_MINUTES * 60:
                continue

            doctor = slot.schedule.doctor
            result.append(SlotInfo(
                slot_id=str(slot.id),
                doctor_id=str(doctor.id),
                date=slot.slot_date,
                start_time=slot.start_time,
                end_time=slot.end_time,
                is_booked=slot.is_booked,
                doctor_name=doctor.user.full_name,
                specialty=doctor.get_specialty_display(),
            ))

        return result


    def check_conflict(self, patient_id: str, slot_id: str) -> bool:
     
        from .models import Appointment

        try:
            slot = self._TimeSlot.objects.get(pk=slot_id)
        except self._TimeSlot.DoesNotExist:
            raise SlotNotAvailableError(f"Slot {slot_id} không tồn tại.")

        # Lấy các lịch hẹn của patient vào cùng ngày, chưa huỷ
        existing = (
            self._Appointment.objects
            .filter(
                patient_id=patient_id,
                slot__slot_date=slot.slot_date,
            )
            .exclude(status__in=["cancelled", "no_show"])
            .select_related("slot")
        )

        for apt in existing:
            ex_start = apt.slot.start_time
            ex_end   = apt.slot.end_time
            # Kiểm tra overlap: không overlap khi end <= start hoặc start >= end
            if not (slot.end_time <= ex_start or slot.start_time >= ex_end):
                return True   # có xung đột

        return False

    @log_execution(level="INFO")
    @audit_action("BOOK_APPOINTMENT", model_name="Appointment")
    def book_slot(
        self,
        slot_id: str,
        patient,          # Patient instance
        symptoms: str = "",
        note: str = "",
        user=None,        # User instance — dùng bởi @audit_action
    ) -> BookingResult:
   
        # Validation ngày
        today = date.today()
        max_date = today + timedelta(days=self.MAX_ADVANCE_DAYS)

        try:
            with transaction.atomic():
                # Lock slot — chỉ 1 transaction được đọc tại một thời điểm
                slot = (
                    self._TimeSlot.objects
                    .select_for_update()
                    .get(pk=slot_id)
                )

                # Guard: đã bị đặt
                if slot.is_booked:
                    return BookingResult(
                        success=False,
                        error="Slot này vừa được người khác đặt. Vui lòng chọn slot khác.",
                    )

                # Guard: ngày quá xa
                if slot.slot_date > max_date:
                    return BookingResult(
                        success=False,
                        error=f"Chỉ có thể đặt lịch trong vòng {self.MAX_ADVANCE_DAYS} ngày tới.",
                    )

                # Guard: xung đột lịch
                if self.check_conflict(str(patient.id), slot_id):
                    return BookingResult(
                        success=False,
                        error="Bạn đã có lịch hẹn khác trong khung giờ này.",
                    )

                # Tạo Appointment
                appointment = self._Appointment.objects.create(
                    patient=patient,
                    doctor=slot.schedule.doctor,
                    slot=slot,
                    symptoms=symptoms,
                    note=note,
                    status="pending",
                )

                # Đánh dấu slot đã đặt
                slot.is_booked = True
                slot.save(update_fields=["is_booked"])

                # Invalidate cache slots của doctor ngày đó
                self.get_available_slots(
                    doctor_id=str(slot.schedule.doctor_id),
                    on_date=slot.slot_date,
                    invalidate_cache=True,
                )

                logger.info(
                    "book_slot: appointment=%s  patient=%s  slot=%s",
                    appointment.id, patient.id, slot_id,
                )

                return BookingResult(
                    success=True,
                    appointment_id=str(appointment.id),
                    slot=SlotInfo(
                        slot_id=slot_id,
                        doctor_id=str(slot.schedule.doctor_id),
                        date=slot.slot_date,
                        start_time=slot.start_time,
                        end_time=slot.end_time,
                        is_booked=True,
                    ),
                )

        except self._TimeSlot.DoesNotExist:
            return BookingResult(success=False, error=f"Slot {slot_id} không tồn tại.")
        except Exception as exc:
            logger.exception("book_slot unexpected error: %s", exc)
            return BookingResult(success=False, error="Lỗi hệ thống. Vui lòng thử lại.")

    # ── 5. RELEASE SLOT ──────────────────────────────────────

    @log_execution(level="INFO")
    @require_role("patient", "doctor", "admin")
    @audit_action("CANCEL_APPOINTMENT", model_name="Appointment")
    def release_slot(
        self,
        appointment,      # Appointment instance
        reason: str = "",
        user=None,
    ) -> bool:
        """
        Huỷ lịch hẹn và trả slot về trống.
        Chỉ cho phép huỷ nếu còn >= 2 giờ trước giờ hẹn.

        Returns:
            True nếu huỷ thành công.

        Raises:
            PermissionDeniedError nếu huỷ quá sát giờ hẹn.
        """
        from .decorators import PermissionDeniedError

        slot = appointment.slot
        slot_dt = datetime.combine(slot.slot_date, slot.start_time)
        slot_dt = timezone.make_aware(slot_dt) if timezone.is_naive(slot_dt) else slot_dt
        now     = timezone.now()

        # Không được huỷ khi còn < 2 giờ
        if (slot_dt - now).total_seconds() < 2 * 3600:
            raise PermissionDeniedError(
                "Không thể huỷ lịch khi còn ít hơn 2 giờ trước giờ khám."
            )

        with transaction.atomic():
            appointment.cancel(reason=reason)

        # Invalidate cache
        self.get_available_slots(
            doctor_id=str(slot.schedule.doctor_id),
            on_date=slot.slot_date,
            invalidate_cache=True,
        )

        logger.info(
            "release_slot: appointment=%s  reason='%s'",
            appointment.id, reason,
        )
        return True

    # ── 6. DOCTOR WORKLOAD ───────────────────────────────────

    @cache_result(ttl=300, key_prefix="doctor_workload")
    @log_execution
    def get_doctor_workload(
        self,
        doctor_id: str,
        from_date: date,
        to_date: date,
    ) -> DoctorWorkload:
        """
        Tính thống kê workload của bác sĩ trong khoảng ngày.
        Cache 5 phút — dùng cho dashboard admin.
        """
        from django.db.models import Count, Q

        doctor = (
            self._Doctor.objects
            .select_related("user")
            .get(pk=doctor_id)
        )

        # Tổng slot trong khoảng ngày
        total_slots = self._TimeSlot.objects.filter(
            schedule__doctor_id=doctor_id,
            slot_date__range=(from_date, to_date),
        ).count()

        # Thống kê appointments theo status
        stats = (
            self._Appointment.objects
            .filter(
                doctor_id=doctor_id,
                slot__slot_date__range=(from_date, to_date),
            )
            .aggregate(
                booked=Count("id"),
                completed=Count("id", filter=Q(status="completed")),
                cancelled=Count("id", filter=Q(status="cancelled")),
                no_show=Count("id",   filter=Q(status="no_show")),
            )
        )

        return DoctorWorkload(
            doctor_id=str(doctor.id),
            doctor_name=doctor.user.full_name,
            total_slots=total_slots,
            booked_slots=stats["booked"],
            completed=stats["completed"],
            cancelled=stats["cancelled"],
            no_show=stats["no_show"],
        )