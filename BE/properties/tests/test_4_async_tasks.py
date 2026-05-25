from datetime import timedelta
from django.utils import timezone
from django.test import override_settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from unittest.mock import patch, MagicMock
from rest_framework import status
from rest_framework.test import APITestCase

from properties.models import (
    Property, District, Category, Ward, PropertyManager, 
    ViewingAppointment, ComparisonList
)
from properties.tasks import BackgroundTaskManager, send_appointment_email_task
from housing_project.celery import app

User = get_user_model()

@override_settings(
    CELERY_TASK_ALWAYS_EAGER=True,
    CELERY_TASK_EAGER_PROPAGATES=True,
    CELERY_BROKER_URL='memory://',
    CELERY_RESULT_BACKEND='cache+memory://'
)
class BookingComparisonTests(APITestCase):
    def setUp(self):
        # Lưu trữ trạng thái cấu hình celery cũ
        self.old_conf = {
            'task_always_eager': app.conf.task_always_eager,
            'task_eager_propagates': app.conf.task_eager_propagates,
            'broker_url': app.conf.broker_url,
            'result_backend': app.conf.result_backend,
        }

        # Ép buộc Celery chạy đồng bộ và in-memory hoàn toàn để tránh kết nối tới Redis
        app.conf.update(
            task_always_eager=True,
            task_eager_propagates=True,
            broker_url='memory://',
            result_backend='cache+memory://'
        )

        # Tạo người dùng thử nghiệm
        self.guest = User.objects.create_user(username="guest_user", email="guest@example.com", password="pwd")  # type: ignore
        self.landlord = User.objects.create_user(username="landlord_user", email="landlord@example.com", password="pwd")  # type: ignore

        # Tạo metadata
        self.district = District.objects.create(name="Liên Chiểu")
        self.ward = Ward.objects.create(name="Hòa Khánh Bắc", district=self.district)
        self.category = Category.objects.create(name="Căn hộ", slug="can-ho")

        # Tạo 2 phòng trọ để so sánh
        self.property = Property.objects.create(
            title="Phòng trọ 1", price=2500000, area=25.0, district=self.district, 
            ward=self.ward, category=self.category, source_name="NhaTot", source_url="http://example.com/p1", is_active=True
        )
        self.property_compare = Property.objects.create(
            title="Phòng trọ 2", price=3000000, area=30.0, district=self.district, 
            ward=self.ward, category=self.category, source_name="NhaTot", source_url="http://example.com/p2", is_active=True
        )

        # Gán phòng cho chủ trọ
        PropertyManager.objects.create(property=self.property, landlord=self.landlord)
        PropertyManager.objects.create(property=self.property_compare, landlord=self.landlord)

        # Endpoints
        self.appointment_list_url = "/api/appointments/"
        self.compare_url = "/api/compare/"
        cache.clear()

    def tearDown(self):
        # Hoàn trả trạng thái cấu hình celery
        app.conf.update(self.old_conf)

    def test_appointment_booking_and_status_update(self):
        self.client.force_authenticate(user=self.guest)
        future_date = timezone.now() + timedelta(days=2)
        
        # 1. Đặt lịch hẹn thành công (Happy path)
        data = {
            "property": self.property.id,
            "appointment_date": future_date.isoformat(),
            "note": "Xem phòng chiều mai"
        }
        res = self.client.post(self.appointment_list_url, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        appointment_id = res.data["id"]

        # 2. Khách thuê cố tình xác nhận lịch -> Bị từ chối 403 Forbidden
        url = f"{self.appointment_list_url}{appointment_id}/"
        res_guest_patch = self.client.patch(url, {"status": "CONFIRMED"})
        self.assertEqual(res_guest_patch.status_code, status.HTTP_403_FORBIDDEN)

        # 3. Chủ trọ xác nhận lịch -> Thành công 200 OK
        self.client.force_authenticate(user=self.landlord)
        res_landlord_patch = self.client.patch(url, {"status": "CONFIRMED"})
        self.assertEqual(res_landlord_patch.status_code, status.HTTP_200_OK)
        
        db_appt = ViewingAppointment.objects.get(id=appointment_id)
        self.assertEqual(db_appt.status, "CONFIRMED")

    def test_comparison_list_and_matrix_cache(self):
        self.client.force_authenticate(user=self.guest)

        # 1. Thêm phòng vào danh sách so sánh
        self.client.post(f"{self.compare_url}add/", {"property_id": self.property.id})
        self.client.post(f"{self.compare_url}add/", {"property_id": self.property_compare.id})

        # 2. Lấy ma trận so sánh (Cache Miss)
        res_miss = self.client.get(f"{self.compare_url}matrix/")
        self.assertEqual(res_miss.status_code, status.HTTP_200_OK)
        self.assertEqual(res_miss.data["cache"], "miss")

        # 3. Lấy ma trận so sánh lần 2 (Cache Hit)
        res_hit = self.client.get(f"{self.compare_url}matrix/")
        self.assertEqual(res_hit.status_code, status.HTTP_200_OK)
        self.assertEqual(res_hit.data["cache"], "hit")


@override_settings(
    CELERY_TASK_ALWAYS_EAGER=True,
    CELERY_TASK_EAGER_PROPAGATES=True,
    CELERY_BROKER_URL='memory://',
    CELERY_RESULT_BACKEND='cache+memory://'
)
class CeleryTasksTests(APITestCase):
    def setUp(self):
        self.old_conf = {
            'task_always_eager': app.conf.task_always_eager,
            'task_eager_propagates': app.conf.task_eager_propagates,
            'broker_url': app.conf.broker_url,
            'result_backend': app.conf.result_backend,
        }

        app.conf.update(
            task_always_eager=True,
            task_eager_propagates=True,
            broker_url='memory://',
            result_backend='cache+memory://'
        )

        self.guest = User.objects.create_user(username="t_guest", email="g@t.com", password="pwd")  # type: ignore
        self.landlord = User.objects.create_user(username="t_lord", email="l@t.com", password="pwd")  # type: ignore
        
        self.district = District.objects.create(name="Hải Châu")
        self.ward = Ward.objects.create(name="Thạch Thang", district=self.district)
        self.category = Category.objects.create(name="Căn hộ", slug="can-ho")
        self.property = Property.objects.create(
            title="Nhà trọ task test", price=2500000, area=25.0, district=self.district, 
            ward=self.ward, category=self.category, source_url="http://t.com/task", is_active=True
        )
        self.appointment = ViewingAppointment.objects.create(
            property=self.property, guest=self.guest, landlord=self.landlord,
            appointment_date=timezone.now() + timedelta(days=1), status="PENDING"
        )

    def tearDown(self):
        app.conf.update(self.old_conf)

    @patch("django.core.mail.send_mail")
    def test_send_appointment_email_task(self, mock_send_mail):
        # Chạy trực tiếp task gửi mail xem có gọi hàm gửi mail của Django không
        res = send_appointment_email_task(self.appointment.id)
        self.assertTrue(res)
        mock_send_mail.assert_called_once()

    @patch("properties.tasks.PropertyImportService")
    def test_background_task_manager(self, mock_service_class):
        # Mock class PropertyImportService
        mock_service = mock_service_class.return_value
        mock_service.import_data.return_value = {"created": 1, "updated": 0, "skipped": 0}

        manager = BackgroundTaskManager()
        task = manager.start_import_properties("dummy_path.csv")
        
        self.assertIsNotNone(task)
        self.assertEqual(task["status"], "success")
        self.assertEqual(task["result"], {"created": 1, "updated": 0, "skipped": 0})
