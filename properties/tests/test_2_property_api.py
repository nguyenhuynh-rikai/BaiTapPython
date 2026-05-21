from rest_framework import status
from rest_framework.test import APITestCase
from properties.models import Property, District, Category, Ward, Amenity

class PropertyAPITests(APITestCase):
    def setUp(self):
        self.district = District.objects.create(name="Liên Chiểu")
        self.ward = Ward.objects.create(name="Hòa Khánh Bắc", district=self.district)
        self.category = Category.objects.create(name="Căn hộ", slug="can-ho")
        self.amenity = Amenity.objects.create(name="Wifi")
        
        self.property = Property.objects.create(
            title="Căn hộ cao cấp Hòa Khánh",
            description="Phòng rộng, thoáng mát, gần trường Đại học Bách Khoa",
            price=2500000,
            area=30.0,
            latitude=16.08,
            longitude=108.15,
            district=self.district,
            ward=self.ward,
            category=self.category,
            source_name="NhaTot",
            source_url="http://example.com/prop-test-2",
            is_active=True
        )
        self.property.amenities.add(self.amenity)
        self.list_url = "/api/properties/"

    def test_property_filters_and_coverage(self):
        # 1. Test lọc theo District, Ward, Category, Price, Area, Source
        params = {
            "district": "Liên Chiểu",
            "ward": "Hòa Khánh Bắc",
            "category": "can-ho",
            "min_price": 1000000,
            "max_price": 3000000,
            "min_area": 20,
            "max_area": 40,
            "source": "NhaTot"
        }
        res = self.client.get(self.list_url, params)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

        # 2. Test lọc địa lý theo Bounding Box (in_bbox = min_lon,min_lat,max_lon,max_lat)
        # Tọa độ phòng: 16.08, 108.15. Hộp giới hạn bao quanh: 108.0 đến 108.3 và 16.0 đến 16.2
        bbox_params = {"in_bbox": "108.0,16.0,108.3,16.2"}
        res_bbox = self.client.get(self.list_url, bbox_params)
        self.assertEqual(res_bbox.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_bbox.data), 1)

        # 3. Test lọc bbox sai định dạng (kiểm tra khả năng bắt lỗi của views)
        res_bad_bbox = self.client.get(self.list_url, {"in_bbox": "108.0,16.0"})
        self.assertEqual(res_bad_bbox.status_code, status.HTTP_200_OK)

        # 4. Test tìm kiếm Full-text search (?search=...)
        res_search = self.client.get(self.list_url, {"search": "Bách Khoa"})
        self.assertEqual(res_search.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_search.data), 1)

    def test_property_details_and_simple_endpoints(self):
        # 1. Test xem chi tiết phòng
        url = f"{self.list_url}{self.property.id}/"
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["title"], "Căn hộ cao cấp Hòa Khánh")

        # 2. Test các API phụ trợ lấy danh mục quận huyện, phường xã
        endpoints = ["/api/categories/", "/api/districts/", "/api/wards/", "/api/amenities/"]
        for endpoint in endpoints:
            res = self.client.get(endpoint)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
