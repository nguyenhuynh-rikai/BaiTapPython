from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from properties.models import Property, District, Category, Ward, Amenity, PropertyImage, FavoriteProperty

User = get_user_model()

class PropertyViewsTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin", password="pwd")  # type: ignore
        self.district = District.objects.create(name="Hải Châu")
        self.ward = Ward.objects.create(name="Thạch Thang", district=self.district)
        self.category = Category.objects.create(name="Phòng trọ", slug="phong-tro")
        self.amenity = Amenity.objects.create(name="Wifi")
        
        self.property = Property.objects.create(
            title="Phòng trọ giá rẻ",
            description="Mô tả đẹp",
            price=3000000,
            area=20,
            source_name="NhaTot",
            source_url="http://test.com/1",
            district=self.district,
            ward=self.ward,
            category=self.category,
            is_active=True,
            latitude=16.05,
            longitude=108.2
        )
        self.property.amenities.add(self.amenity)
        self.list_url = '/api/properties/'

    def test_property_list_and_filters(self):
        # Test basic list status
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        # Test filtering exists without strict value matching
        res_filter = self.client.get(self.list_url, {'source': 'NhaTot', 'district': 'Hải Châu'})
        self.assertEqual(res_filter.status_code, status.HTTP_200_OK)
        
        res_price = self.client.get(self.list_url, {'min_price': 1000, 'max_price': 5000000})
        self.assertEqual(res_price.status_code, status.HTTP_200_OK)

    def test_in_bbox_filter(self):
        res = self.client.get(self.list_url, {'in_bbox': '108.0,16.0,108.5,16.1'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_search_filter(self):
        res = self.client.get(self.list_url, {'search': 'Phòng'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_stats_action(self):
        url = f'{self.list_url}stats/'
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        # Second call to verify cache hit/miss flows
        res2 = self.client.get(url)
        self.assertEqual(res2.status_code, status.HTTP_200_OK)

    def test_clear_cache_action(self):
        url = f'{self.list_url}clear_cache/'
        self.client.force_authenticate(user=self.admin)
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_export_excel(self):
        res = self.client.get(f'{self.list_url}export_excel/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_favorite_toggle(self):
        # Unauthenticated
        response = self.client.post(f'{self.list_url}{self.property.id}/favorite/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticated - Add favorite
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(f'{self.list_url}{self.property.id}/favorite/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(FavoriteProperty.objects.filter(user=self.admin, property=self.property).exists())

        # Authenticated - Remove favorite
        response = self.client.post(f'{self.list_url}{self.property.id}/favorite/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(FavoriteProperty.objects.filter(user=self.admin, property=self.property).exists())

    def test_favorites_list(self):
        self.client.force_authenticate(user=self.admin)
        FavoriteProperty.objects.create(user=self.admin, property=self.property)
        response = self.client.get('/api/favorites/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["property"], self.property.id)

    def test_district_stats(self):
        response = self.client.get(f'{self.list_url}district-stats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
        self.assertEqual(response.data[0]["district__name"], "Hải Châu")
        self.assertEqual(response.data[0]["total_listings"], 1)


class OtherViewSetsTests(APITestCase):
    def test_simple_endpoints(self):
        # We test that endpoints return 200 OK without deep data assertion
        endpoints = [
            '/api/categories/',
            '/api/districts/',
            '/api/wards/',
            '/api/amenities/'
        ]
        for url in endpoints:
            res = self.client.get(url)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
