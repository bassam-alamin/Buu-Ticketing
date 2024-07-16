import random
from datetime import date
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from apps.booking.models import Theater, TheatreSession


class TheaterViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword',
            is_staff=True)
        self.client.force_authenticate(user=self.user)
        self.theater_data = {
            'name': 'Test Theater',
            'number_of_seats': random.randint(10, 50)
        }

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
        self.theater = Theater.objects.create(
            name='Test Theater',
            number_of_seats=random.randint(10, 50)
        )
        available_seats = list(range(1, self.theater.number_of_seats + 1))
        self.seating = TheatreSession.objects.create(
            theater=self.theater,
            name_of_show="test show",
            date=date(2024, 7, 17),
            available_seats=available_seats
        )
        self.reservation_data = {
                "seat_number":  random.randint(10,self.theater.number_of_seats),
                "seating": f"{self.seating.id}"
            }
        print(self.reservation_data)


    def test_create_reservation(self):
        response = self.client.post(reverse('reservation-view'), self.reservation_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_reservation_details(self):
        self.user.is_staff = True
        self.user.save()
        response = self.client.get(reverse('list-reservations-view'), {'seating_id': f'{self.seating.id}'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_reservation_details_unauthorized(self):
        response = self.client.get(reverse('list-reservations-view'), {'seating_id': f'{self.seating.id}'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
