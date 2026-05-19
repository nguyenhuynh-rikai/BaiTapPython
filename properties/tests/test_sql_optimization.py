# pyrefly: ignore [missing-import]
from django.test import TestCase
# pyrefly: ignore [missing-import]
from rest_framework.test import APIClient
from properties.models import Property, District, Category, Ward, Amenity

class SQLQueryOptimizationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.district = District.objects.create(name="District Test")
        self.category = Category.objects.create(name="Cat Test", slug="cat-test")
        self.ward = Ward.objects.create(name="Ward Test", district=self.district)
        self.amenity = Amenity.objects.create(name="Wifi")

    def create_dummy_property(self, unique_suffix):
        p = Property.objects.create(
            title=f"Property {unique_suffix}",
            source_url=f"http://test-{unique_suffix}.com",
            price=1000,
            area=50,
            district=self.district,
            category=self.category,
            ward=self.ward,
            is_active=True
        )
        p.amenities.add(self.amenity)
        return p

    def test_properties_list_prevents_n_plus_one_queries(self):
        """
        Kiểm tra và chứng minh hệ thống đã ngăn chặn triệt để lỗi N+1 Query.
        Số lượng câu lệnh SQL truy vấn danh sách bài đăng phải giữ nguyên không đổi
        dù trong database có 1 hay nhiều bài đăng.
        """
        import json
        # 1. Tạo 1 bài đăng đầu tiên
        self.create_dummy_property("first")

        # Đo số lượng truy vấn khi lấy danh sách chứa 1 bài đăng
        with self.assertNumQueries(3):
            # 1 query lấy properties + 1 query lấy amenities + 1 query lấy images
            response = self.client.get('/api/properties/')
            self.assertEqual(response.status_code, 200)

        # 2. Tạo thêm 4 bài đăng nữa (Tổng cộng có 5 bài đăng)
        for i in range(4):
            self.create_dummy_property(f"more-{i}")

        # Đo số lượng truy vấn khi lấy danh sách chứa 5 bài đăng
        # Số lượng truy vấn SQL BẮT BUỘC vẫn phải là 3, không được tăng lên theo số lượng bài đăng!
        with self.assertNumQueries(3):
            response = self.client.get('/api/properties/')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.content)
            self.assertEqual(len(data), 5)
