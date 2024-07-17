from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class RegisterViewTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.valid_user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'first_name': 'testfirstname',
            'email': 'testuser@example.com'
        }
        self.invalid_user_data = {
            'username': '',
            'password': 'testpassword',
            'email': 'testuser@example.com'
        }

    def test_register_user_with_valid_data(self):
        response = self.client.post(self.register_url, self.valid_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_register_user_with_invalid_data(self):
        response = self.client.post(self.register_url, self.invalid_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)


class LoginViewTests(APITestCase):
    def setUp(self):
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com'
        )
        self.valid_login_data = {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        self.invalid_login_data = {
            'email': 'testuser+2@example.com',
            'password': 'wrongpassword'
        }

    def test_login_user_with_valid_data(self):
        response = self.client.post(self.login_url, self.valid_login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('jwt_token', response.data)

    def test_login_user_with_invalid_data(self):
        response = self.client.post(self.login_url, self.invalid_login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('jwt_token', response.data)
