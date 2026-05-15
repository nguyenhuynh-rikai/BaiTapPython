"""
MediFlow — tests/test_business_logic.py
=========================================
Unit tests cho decorators và SlotEngine.
Chạy không cần database thật (dùng mock / unittest.mock).

    python -m pytest tests/test_business_logic.py -v
"""

import time
import unittest
from datetime import date, timedelta
from unittest.mock import MagicMock, patch, PropertyMock


# ─────────────────────────────────────────────────────────────
# TEST: DECORATORS
# ─────────────────────────────────────────────────────────────

class TestLogExecution(unittest.TestCase):

    def test_returns_value_normally(self):
        """@log_execution không thay đổi giá trị trả về."""
        import sys, os
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from decorators import log_execution

        @log_execution
        def add(a, b):
            return a + b

        self.assertEqual(add(2, 3), 5)

    def test_re_raises_exception(self):
        """@log_execution phải re-raise exception gốc."""
        from decorators import log_execution

        @log_execution
        def broken():
            raise ValueError("test error")

        with self.assertRaises(ValueError):
            broken()

    def test_preserves_function_name(self):
        """functools.wraps phải giữ __name__ và __doc__."""
        from decorators import log_execution

        @log_execution
        def my_function():
            """docstring."""
            pass

        self.assertEqual(my_function.__name__, "my_function")
        self.assertEqual(my_function.__doc__, "docstring.")

    def test_timing_roughly_correct(self):
        """Decorator không làm chậm hơn 50ms so với hàm trống."""
        from decorators import log_execution

        @log_execution
        def noop():
            pass

        start = time.perf_counter()
        for _ in range(100):
            noop()
        elapsed = time.perf_counter() - start

        self.assertLess(elapsed, 0.05, "100 calls nên < 50ms overhead")


class TestRequireRole(unittest.TestCase):

    def setUp(self):
        import sys, os
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from decorators import require_role, PermissionDeniedError
        self.require_role = require_role
        self.PermissionDeniedError = PermissionDeniedError

    def _make_user(self, role: str):
        user = MagicMock()
        user.role = role
        return user

    def test_allowed_role_passes(self):
        @self.require_role("doctor", "admin")
        def action(user):
            return "ok"

        self.assertEqual(action(user=self._make_user("doctor")), "ok")
        self.assertEqual(action(user=self._make_user("admin")), "ok")

    def test_forbidden_role_raises(self):
        @self.require_role("doctor", "admin")
        def action(user):
            return "ok"

        with self.assertRaises(self.PermissionDeniedError):
            action(user=self._make_user("patient"))

    def test_missing_user_raises_value_error(self):
        @self.require_role("admin")
        def action():
            return "ok"

        with self.assertRaises((ValueError, TypeError)):
            action()

    def test_allowed_roles_stored_on_wrapper(self):
        @self.require_role("doctor")
        def action(user):
            pass

        self.assertEqual(action._allowed_roles, ("doctor",))


class TestCacheResult(unittest.TestCase):

    def setUp(self):
        import sys, os
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

    def test_second_call_uses_cache(self):
        """Hàm chỉ được gọi 1 lần khi cache hit."""
        from decorators import cache_result, _MEMORY_CACHE
        _MEMORY_CACHE.clear()

        call_count = 0

        with patch("decorators.cache") as mock_cache:
            mock_cache.get.return_value = None   # cache miss lần đầu

            @cache_result(ttl=60, key_prefix="test")
            def expensive(x):
                nonlocal call_count
                call_count += 1
                return x * 2

            expensive(5)
            # Lần 2: giả lập cache hit
            mock_cache.get.return_value = 10
            expensive(5)

        self.assertEqual(call_count, 1)

    def test_no_cache_bypasses(self):
        """no_cache=True luôn gọi lại hàm."""
        from decorators import cache_result, _MEMORY_CACHE
        _MEMORY_CACHE.clear()

        call_count = 0

        with patch("decorators.cache") as mock_cache:
            mock_cache.get.return_value = 99   # có cache

            @cache_result(ttl=60)
            def fn(x):
                nonlocal call_count
                call_count += 1
                return x

            fn(1, no_cache=True)
            fn(1, no_cache=True)

        self.assertEqual(call_count, 2)

    def test_redis_down_falls_back_to_memory(self):
        """Khi Redis lỗi, dùng memory cache."""
        from decorators import cache_result, _MEMORY_CACHE
        _MEMORY_CACHE.clear()

        with patch("decorators.cache") as mock_cache:
            mock_cache.get.side_effect = Exception("Redis down")
            mock_cache.set.side_effect = Exception("Redis down")

            @cache_result(ttl=60, key_prefix="mem_test")
            def fn(x):
                return x + 1

            result = fn(10)

        self.assertEqual(result, 11)
        # Phải có entry trong memory cache
        self.assertTrue(any("mem_test" in k for k in _MEMORY_CACHE))


# ─────────────────────────────────────────────────────────────
# TEST: SLOT ENGINE
# ─────────────────────────────────────────────────────────────

class TestSlotEngineSplitSlots(unittest.TestCase):
    """Test _split_into_slots — không cần DB."""

    def setUp(self):
        import sys, os
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

    def _make_schedule(self, start: str, end: str, duration: int = 30):
        from datetime import time as t
        h, m = map(int, start.split(":"))
        h2, m2 = map(int, end.split(":"))
        schedule = MagicMock()
        schedule.start_time = t(h, m)
        schedule.end_time   = t(h2, m2)
        schedule.slot_duration_min = duration
        return schedule

    def _engine(self):
        with patch("slot_engine.SlotEngine.__init__", lambda self: None):
            from slot_engine import SlotEngine
            engine = SlotEngine.__new__(SlotEngine)
        return engine

    def test_4_slots_in_2_hour_window(self):
        engine   = self._engine()
        schedule = self._make_schedule("08:00", "10:00", 30)
        slots    = engine._split_into_slots(schedule, date.today())
        self.assertEqual(len(slots), 4)

    def test_slot_boundaries_correct(self):
        from datetime import time as t
        engine   = self._engine()
        schedule = self._make_schedule("09:00", "10:30", 30)
        slots    = engine._split_into_slots(schedule, date.today())
        self.assertEqual(slots[0], (t(9, 0),  t(9, 30)))
        self.assertEqual(slots[1], (t(9, 30), t(10, 0)))
        self.assertEqual(slots[2], (t(10, 0), t(10, 30)))

    def test_no_partial_slot_at_end(self):
        """Không tạo slot dở nếu không chia hết."""
        engine   = self._engine()
        schedule = self._make_schedule("08:00", "09:50", 30)
        slots    = engine._split_into_slots(schedule, date.today())
        # 8:00-8:30, 8:30-9:00, 9:00-9:30 — slot 9:30-10:00 không đủ
        self.assertEqual(len(slots), 3)

    def test_empty_when_duration_exceeds_window(self):
        engine   = self._engine()
        schedule = self._make_schedule("08:00", "08:20", 30)
        slots    = engine._split_into_slots(schedule, date.today())
        self.assertEqual(slots, [])


class TestSlotEngineCheckConflict(unittest.TestCase):

    def _make_engine_with_mocks(self, existing_appointments):
        with patch("slot_engine.SlotEngine.__init__", lambda self: None):
            from slot_engine import SlotEngine
            engine = SlotEngine.__new__(SlotEngine)

        mock_slot_qs = MagicMock()
        mock_slot_qs.__iter__ = MagicMock(return_value=iter([]))

        mock_timeslot_model = MagicMock()

        # Slot được kiểm tra
        from datetime import time as t
        target_slot = MagicMock()
        target_slot.slot_date  = date.today()
        target_slot.start_time = t(9, 0)
        target_slot.end_time   = t(9, 30)
        mock_timeslot_model.objects.get.return_value = target_slot

        # Existing appointments của patient
        mock_apt_qs = MagicMock()
        mock_apt_qs.filter.return_value = mock_apt_qs
        mock_apt_qs.exclude.return_value = mock_apt_qs
        mock_apt_qs.select_related.return_value = existing_appointments
        mock_apt_qs.__iter__ = MagicMock(return_value=iter(existing_appointments))

        engine._TimeSlot    = mock_timeslot_model
        engine._Appointment = MagicMock()
        engine._Appointment.objects = mock_apt_qs

        return engine

    def _make_appointment(self, start: str, end: str):
        from datetime import time as t
        h, m   = map(int, start.split(":"))
        h2, m2 = map(int, end.split(":"))
        apt = MagicMock()
        apt.slot.slot_date  = date.today()
        apt.slot.start_time = t(h, m)
        apt.slot.end_time   = t(h2, m2)
        return apt

    def test_no_conflict_when_no_existing(self):
        engine = self._make_engine_with_mocks([])
        result = engine.check_conflict("patient-1", "slot-1")
        self.assertFalse(result)

    def test_conflict_when_overlap(self):
        """9:00-9:30 trùng với 8:50-9:10."""
        existing = [self._make_appointment("08:50", "09:10")]
        engine   = self._make_engine_with_mocks(existing)
        result   = engine.check_conflict("patient-1", "slot-1")
        self.assertTrue(result)

    def test_no_conflict_when_adjacent(self):
        """9:00-9:30 kế tiếp 8:30-9:00 — không trùng."""
        existing = [self._make_appointment("08:30", "09:00")]
        engine   = self._make_engine_with_mocks(existing)
        result   = engine.check_conflict("patient-1", "slot-1")
        self.assertFalse(result)

    def test_no_conflict_when_after(self):
        """9:00-9:30 trước 9:30-10:00 — không trùng."""
        existing = [self._make_appointment("09:30", "10:00")]
        engine   = self._make_engine_with_mocks(existing)
        result   = engine.check_conflict("patient-1", "slot-1")
        self.assertFalse(result)


class TestDoctorWorkloadDTO(unittest.TestCase):

    def test_utilization_calculated_correctly(self):
        from slot_engine import DoctorWorkload
        wl = DoctorWorkload(
            doctor_id="x",
            doctor_name="Dr. Test",
            total_slots=20,
            booked_slots=15,
            completed=10,
            cancelled=3,
            no_show=2,
        )
        self.assertEqual(wl.utilization_pct, 75.0)

    def test_zero_total_slots_no_division_error(self):
        from slot_engine import DoctorWorkload
        wl = DoctorWorkload(
            doctor_id="x",
            doctor_name="Dr. Test",
            total_slots=0,
            booked_slots=0,
            completed=0,
            cancelled=0,
            no_show=0,
        )
        self.assertEqual(wl.utilization_pct, 0.0)


class TestAppointmentDTO(unittest.TestCase):

    def test_to_dict_serializable(self):
        import json
        from appointment_service import AppointmentDTO

        dto = AppointmentDTO(
            id="abc",
            patient_name="Nguyễn Văn A",
            doctor_name="BS. Trần Thị B",
            specialty="Đa khoa",
            clinic_name="Phòng khám 1",
            slot_date="2026-06-01",
            start_time="09:00",
            end_time="09:30",
            status="pending",
            symptoms="Đau đầu",
            consultation_fee="200,000đ",
            booked_at="2026-05-14 08:00",
        )

        d = dto.to_dict()
        self.assertIsInstance(d, dict)
        # Phải JSON serializable
        json.dumps(d)
        self.assertEqual(d["status"], "pending")
        self.assertEqual(d["start_time"], "09:00")


if __name__ == "__main__":
    unittest.main(verbosity=2)