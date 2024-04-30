from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from .serializers import UserSerializer
from .manage_token import *
from .models import User


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        url = reverse('register')
        data = {
            'email': 'test@example.com',
            'password': 'password123',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"id": 1, "email": "test@example.com"})


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        serializer = UserSerializer(
            data={
                'email': 'test@example.com',
                'password': 'password123',
            }
        )
        serializer.is_valid()
        self.user = serializer.save()

    def test_login_user(self):
        url = reverse('login')
        data = {
            'email': 'test@example.com',
            'password': 'password123',
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

        refresh_token = response.data['refresh_token']
        refresh_token_from_db = RefreshToken.objects.filter(token=refresh_token).first()

        self.assertEqual(refresh_token, str(refresh_token_from_db.token))

    def test_get_user(self):
        refresh_token = create_refresh_token(self.user)
        access_token = get_access_by_refresh(refresh_token)
        url = reverse('me')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        refresh_token = create_refresh_token(self.user)
        access_token = get_access_by_refresh(refresh_token)
        url = reverse('me')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        data = {
            "username": "test",
        }
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {
                "id": 1,
                "email": "test@example.com",
                "username": "test",
            }
        )


class RefreshViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='test@example.com', password='password123')
        self.refresh_token = create_refresh_token(self.user)

    def test_refresh_token(self):
        url = reverse('refresh')
        data = {
            'refresh_token': self.refresh_token,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='test@example.com', password='password123')
        self.refresh_token = create_refresh_token(self.user)

    def test_logout_user(self):
        url = reverse('logout')
        data = {
            'refresh_token': self.refresh_token,
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"success": "User logged out."})

        refresh_token_from_db = RefreshToken.objects.filter(token=self.refresh_token).first()
        self.assertEqual(None, refresh_token_from_db)
