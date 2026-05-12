from django.contrib.auth.models import User  # Thêm import này
from rest_framework.test import APITestCase, APIClient
from .models import Interns
from rest_framework import status
from django.urls import reverse

# ... các import cũ

class InternAPITests(APITestCase):
    def setUp(self):
        # 1. Tạo một user giả để test
        self.user = User.objects.create_superuser(username='admin', password='password123', email='a@a.com')

        # 2. Tạo dữ liệu mẫu
        self.intern = Interns.objects.create(
            name="Test Intern",
            email="test@gmail.com",
            specialization="Backend"
        )
        self.list_url = reverse('interns-list')

        # 3. ÉP XÁC THỰC: Luôn đăng nhập bằng user này cho mọi bài test
        self.client.force_authenticate(user=self.user)

    def test_get_intern_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_intern_invalid(self):
        data = {"name": "N", "email": "n@gmail.com", "specialization": "Frontend"}
        response = self.client.post(self.list_url, data)
        # Bây giờ máy test đã vượt qua cửa 401, nó sẽ chạm được vào logic Validation bài 14 của bạn
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)