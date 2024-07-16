from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse


class TheaterViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword',
            is_staff=True)
        self.client.force_authenticate(user=self.user)
        self.theater_data = {'name': 'Test Theater', 'location': 'Test Location'}

    def test_create_theater(self):
        response = self.client.post(reverse('theatre-view'), self.theater_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_theaters(self):
        response = self.client.get(reverse('list-theaters-view'), {'date': '2024-07-17'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ReservationViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        self.reservation_data = {'seating_id': 'some_uuid_here'}

    def test_create_reservation(self):
        response = self.client.post(reverse('reservation-view'), self.reservation_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_reservation_details(self):
        self.user.is_staff = True
        self.user.save()
        response = self.client.get(reverse('list-reservation-view'), {'seating_id': 'some_uuid_here'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_reservation_details_unauthorized(self):
        response = self.client.get(reverse('list-reservation-view'), {'seating_id': 'some_uuid_here'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
