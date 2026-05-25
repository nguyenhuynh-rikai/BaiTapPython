from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()

class AuthIdentityTests(APITestCase):
    def setUp(self):
        self.register_url = "/api/auth/register/"
        self.login_url = "/api/auth/login/"
        self.profile_url = "/api/auth/profile/"
        self.user_data = {
            "username": "auth_user",
            "email": "auth@example.com",
            "password": "strong_password123",
            "password_confirm": "strong_password123",
            "role": "guest"
        }

    def test_register_and_login_success(self):
        # 1. Đăng ký tài khoản mới
        res_register = self.client.post(self.register_url, self.user_data)
        self.assertEqual(res_register.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_register.data["user"]["username"], "auth_user")

        # 2. Đăng nhập để lấy Token
        login_data = {
            "username": "auth_user",
            "password": "strong_password123"
        }
        res_login = self.client.post(self.login_url, login_data)
        self.assertEqual(res_login.status_code, status.HTTP_200_OK)
        self.assertIn("token", res_login.data)

    def test_profile_permissions(self):
        # Truy cập khi chưa đăng nhập -> 401 Unauthorized
        res_anon = self.client.get(self.profile_url)
        self.assertEqual(res_anon.status_code, status.HTTP_401_UNAUTHORIZED)

        # Đăng nhập và truy cập -> 200 OK
        user = User.objects.create_user(username="test_profile", password="pwd")  # type: ignore
        self.client.force_authenticate(user=user)
        res_auth = self.client.get(self.profile_url)
        self.assertEqual(res_auth.status_code, status.HTTP_200_OK)
