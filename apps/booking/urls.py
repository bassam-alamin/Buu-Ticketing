from django.urls import path

from .views import (TheaterViewSet, TheatreSessionViewSet,
                    ReservationViewSet, ListAvailableSeatsView,
                    ListTheatresView, ReservationDetailsView)


urlpatterns = [
    path('create/theater', TheaterViewSet.as_view(), name='theatre-view'),
    path('create/reservation', ReservationViewSet.as_view(), name='reservation-view'),
    path('create/seating', TheatreSessionViewSet.as_view(), name='session-view'),
    path('list/available/seats', ListAvailableSeatsView.as_view(), name='list-session-view'),
    path('list/available/theaters', ListTheatresView.as_view(), name='list-theaters-view'),
    path('list/reservation/details', ReservationDetailsView.as_view(), name='list-reservations-view')
]
