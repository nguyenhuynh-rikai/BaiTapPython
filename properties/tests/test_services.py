import os
import tempfile
import csv
from django.test import TestCase
from properties.models import Property, Category, District, Ward
from properties.services import (
    safe_text, safe_int, safe_float, is_valid_property_data, 
    calculate_price_per_m2, PropertyImportService
)

class ServicesUtilsTests(TestCase):
    def test_safe_text(self):
        self.assertEqual(safe_text("  hello  "), "hello")
        self.assertEqual(safe_text(None), "")
        self.assertEqual(safe_text(123), "123")

    def test_safe_int(self):
        self.assertEqual(safe_int("123"), 123)
        self.assertEqual(safe_int("123.45"), 123)
        self.assertEqual(safe_int(123.45), 123)
        self.assertIsNone(safe_int("abc"))
        self.assertIsNone(safe_int(None))

    def test_safe_float(self):
        self.assertEqual(safe_float("123.45"), 123.45)
        self.assertEqual(safe_float(123), 123.0)
        self.assertIsNone(safe_float("abc"))
        self.assertIsNone(safe_float(None))

    def test_is_valid_property_data(self):
        self.assertTrue(is_valid_property_data("title", "url", 1000, 50.0))
        self.assertFalse(is_valid_property_data("", "url", 1000, 50.0))
        self.assertFalse(is_valid_property_data("title", "", 1000, 50.0))
        self.assertFalse(is_valid_property_data("title", "url", None, 50.0))
        self.assertFalse(is_valid_property_data("title", "url", 1000, None))

    def test_calculate_price_per_m2(self):
        self.assertEqual(calculate_price_per_m2(1000000, 50), 20000)
        self.assertIsNone(calculate_price_per_m2(None, 50))
        self.assertIsNone(calculate_price_per_m2(1000000, None))
        self.assertIsNone(calculate_price_per_m2(1000000, 0))

class PropertyImportServiceTests(TestCase):
    def setUp(self):
        # Create a temporary CSV file
        self.fd, self.csv_path = tempfile.mkstemp(suffix='.csv')
        with os.fdopen(self.fd, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=[
                "title", "url", "source", "price_vnd", "area_m2", 
                "price_per_m2", "district", "ward", "description", 
                "address", "posted_at"
            ])
            writer.writeheader()
            writer.writerow({
                "title": "Nha tro 1", "url": "http://test.com/1", "source": "Test",
                "price_vnd": "2000000", "area_m2": "20.5", "price_per_m2": "",
                "district": "Hai Chau", "ward": "Thach Thang", "description": "Mo ta 1",
                "address": "123 Le Duan", "posted_at": "Hom nay"
            })
            writer.writerow({
                "title": "Nha tro 2", "url": "http://test.com/1", "source": "Test", # Same URL, should update
                "price_vnd": "2500000", "area_m2": "25", "price_per_m2": "100000",
                "district": "Hai Chau", "ward": "Thuan Phuoc", "description": "Mo ta 2",
                "address": "456 Le Duan", "posted_at": "Hom qua"
            })
            writer.writerow({
                "title": "", "url": "http://test.com/3", "source": "Test", # Invalid, skipped
                "price_vnd": "2000000", "area_m2": "20.5", "price_per_m2": "",
                "district": "Hai Chau", "ward": "Thach Thang", "description": "Mo ta 3",
                "address": "123 Le Duan", "posted_at": "Hom nay"
            })

    def tearDown(self):
        os.remove(self.csv_path)

    def test_import_data(self):
        service = PropertyImportService(self.csv_path)
        stats = service.import_data()
        
        self.assertEqual(stats["created"], 1)
        self.assertEqual(stats["updated"], 1)
        self.assertEqual(stats["skipped"], 1)

        # Check data
        self.assertEqual(Property.objects.count(), 1)
        prop = Property.objects.get(source_url="http://test.com/1")
        self.assertEqual(prop.title, "Nha tro 2")
        self.assertEqual(prop.price, 2500000)
        self.assertEqual(prop.price_per_m2, 100000)
        self.assertEqual(prop.ward.name, "Thuan Phuoc")
        self.assertEqual(prop.district.name, "Hai Chau")
        self.assertEqual(prop.category.slug, "phong-tro")

    def test_get_or_create_ward_without_district(self):
        service = PropertyImportService(self.csv_path)
        ward = service.get_or_create_ward("WardName", None)
        self.assertIsNone(ward)

    def test_get_or_create_district_empty(self):
        service = PropertyImportService(self.csv_path)
        district = service.get_or_create_district("")
        self.assertIsNone(district)
