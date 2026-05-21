import os
import tempfile
import pandas as pd
from io import StringIO
from django.core.management import call_command
from django.core.cache import cache
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from properties.models import Property, District, Category, Ward

class OperationsTests(APITestCase):
    def setUp(self):
        self.district = District.objects.create(name="Liên Chiểu")
        self.ward = Ward.objects.create(name="Hòa Khánh Bắc", district=self.district)
        self.category = Category.objects.create(name="Căn hộ", slug="can-ho")
        
        self.property = Property.objects.create(
            title="Căn hộ 1",
            price=2500000,
            area=30.0,
            district=self.district,
            ward=self.ward,
            category=self.category,
            source_name="NhaTot",
            source_url="http://example.com/prop-op-test",
            is_active=True
        )
        self.export_url = "/api/properties/export_excel/"

    def test_export_excel(self):
        res = self.client.get(self.export_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Kiểm tra header Content-Type của file Excel trả về
        self.assertEqual(res["Content-Type"], "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    def test_signals_cache_invalidation(self):
        from properties.cache_utils import PROPERTY_CACHE_VERSION_KEY
        # 1. Gán key cache giả định
        cache.set(PROPERTY_CACHE_VERSION_KEY, 1)
        
        # 2. Thay đổi Property để kích hoạt post_save signal
        self.property.title = "Căn hộ 1 đã sửa"
        self.property.save()

        # 3. Kích hoạt signal -> cache version phải tăng lên
        version = cache.get(PROPERTY_CACHE_VERSION_KEY)
        self.assertNotEqual(version, 1)


class CLICommandTests(TestCase):
    def setUp(self):
        # Tạo file CSV tạm thời cực nhỏ để test CLI nhanh nhất có thể
        self.temp_dir = tempfile.TemporaryDirectory()
        self.csv_path = os.path.join(self.temp_dir.name, "test_import.csv")
        df = pd.DataFrame({
            "title": ["Phòng trọ giá rẻ Hải Châu"],
            "url": ["http://example.com/cli-imported-prop"],
            "description": ["Đẹp"],
            "price_vnd": [2000000],
            "area_m2": [25.0],
            "price_per_m2": [80000],
            "address": ["123 Lê Duẩn"],
            "district": ["Hải Châu"],
            "ward": ["Thạch Thang"],
            "source": ["Chotot"],
            "posted_at": ["Hôm qua"]
        })
        df.to_csv(self.csv_path, index=False)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_import_csv_command_success(self):
        # Đảm bảo sạch dữ liệu trước khi test để tránh ảnh hưởng bởi DB cũ
        Property.objects.filter(source_url="http://example.com/cli-imported-prop").delete()

        # Gọi CLI command của Django
        out = StringIO()
        call_command("import_csv", "--file", self.csv_path, stdout=out)

        # Kiểm tra đầu ra CLI báo thành công
        self.assertIn("Thành công!", out.getvalue())

        # Kiểm tra xem dữ liệu đã được import thành công vào DB chưa
        self.assertTrue(Property.objects.filter(source_url="http://example.com/cli-imported-prop").exists())
        imported = Property.objects.get(source_url="http://example.com/cli-imported-prop")
        self.assertEqual(imported.title, "Phòng trọ giá rẻ Hải Châu")
        self.assertIsNotNone(imported.district, "District should not be None")
        self.assertEqual(imported.district.name, "Hải Châu")
