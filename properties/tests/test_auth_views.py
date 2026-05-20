from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class AuthViewsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="TestPassword123!")  # type: ignore
        self.token = Token.objects.create(user=self.user)
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/login/'
        self.change_password_url = '/api/auth/change-password/'
        self.logout_url = '/api/auth/logout/'

    def test_register_view(self):
        data = {
            "username": "newuser",
            "email": "new@test.com",
            "password": "StrongPassword123!",
            "password_confirm": "StrongPassword123!"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["user"]["username"], "newuser")

    def test_login_view(self):
        data = {
            "username": "testuser",
            "password": "TestPassword123!"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_change_password_view(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {
            "old_password": "TestPassword123!",
            "new_password": "NewStrongPassword123!",
            "new_password_confirm": "NewStrongPassword123!"
        }
        response = self.client.post(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_logout_view(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_get_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")

    def test_put_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {
            "first_name": "UpdatedName",
            "last_name": "User",
            "email": "updated@test.com"
        }
        response = self.client.put('/api/auth/profile/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "UpdatedName")
        self.assertEqual(self.user.email, "updated@test.com")

    def test_profile_unauthenticated(self):
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

