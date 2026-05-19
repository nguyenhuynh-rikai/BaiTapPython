from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from properties.auth_serializers import RegisterSerializer, LoginSerializer, ChangePasswordSerializer

User = get_user_model()

class AuthSerializersTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="TestPassword123!")
        self.factory = RequestFactory()

    def test_register_serializer_valid(self):
        data = {
            "username": "newuser",
            "email": "new@test.com",
            "password": "StrongPassword123!",
            "password_confirm": "StrongPassword123!"
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, "newuser")
        self.assertTrue(user.check_password("StrongPassword123!"))

    def test_register_serializer_username_exists(self):
        data = {
            "username": "testuser",
            "password": "StrongPassword123!",
            "password_confirm": "StrongPassword123!"
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)

    def test_register_serializer_password_mismatch(self):
        data = {
            "username": "newuser",
            "password": "StrongPassword123!",
            "password_confirm": "DifferentPassword123!"
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password_confirm", serializer.errors)
        self.assertEqual(serializer.errors["password_confirm"][0], "Passwords khong khop.")

    def test_login_serializer_valid(self):
        request = self.factory.post('/login')
        data = {
            "username": "testuser",
            "password": "TestPassword123!"
        }
        serializer = LoginSerializer(data=data, context={"request": request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["user"], self.user)

    def test_login_serializer_invalid(self):
        request = self.factory.post('/login')
        data = {
            "username": "testuser",
            "password": "WrongPassword123!"
        }
        serializer = LoginSerializer(data=data, context={"request": request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(serializer.errors["non_field_errors"][0], "Sai username hoac password.")

    def test_change_password_serializer_valid(self):
        request = self.factory.post('/change-password')
        request.user = self.user
        data = {
            "old_password": "TestPassword123!",
            "new_password": "NewStrongPassword123!",
            "new_password_confirm": "NewStrongPassword123!"
        }
        serializer = ChangePasswordSerializer(data=data, context={"request": request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertTrue(user.check_password("NewStrongPassword123!"))

    def test_change_password_serializer_wrong_old(self):
        request = self.factory.post('/change-password')
        request.user = self.user
        data = {
            "old_password": "WrongPassword!",
            "new_password": "NewStrongPassword123!",
            "new_password_confirm": "NewStrongPassword123!"
        }
        serializer = ChangePasswordSerializer(data=data, context={"request": request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("old_password", serializer.errors)

    def test_change_password_serializer_mismatch(self):
        request = self.factory.post('/change-password')
        request.user = self.user
        data = {
            "old_password": "TestPassword123!",
            "new_password": "NewStrongPassword123!",
            "new_password_confirm": "Mismatch!"
        }
        serializer = ChangePasswordSerializer(data=data, context={"request": request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("new_password_confirm", serializer.errors)
