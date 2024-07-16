from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Theater, TheatreSession, Reservation
from django.contrib.auth.models import User


class TheaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theater
        fields = "__all__"
        read_only_fields = ("id",)


class TheatreSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreSession
        fields = "__all__"
        read_only_fields = ("available_seats","id",)

    def create(self, validated_data):
        theater = validated_data.get('theater')
        date = validated_data["date"]
        session = TheatreSession.objects.filter(
            theater=theater, date=date
        )
        if session.exists():
            raise ValidationError(
                f"Theater already has a session on date {date}"
            )
        available_seats = list(range(1, theater.number_of_seats + 1))
        theatre_session = TheatreSession.objects.create(
            available_seats=available_seats,
            **validated_data
        )
        return theatre_session


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"
        read_only_fields = ("user","id",)

    def create(self, validated_data):
        theater_session = validated_data["seating"]
        if not theater_session:
            raise ValidationError("Enter a valid Seating")
        if validated_data["seat_number"] not in theater_session.available_seats:
            raise ValidationError("This seat is not available. Choose another seat")
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = User.objects.get(id=representation.pop("user"))
        representation["user_details"] = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }
        return representation
