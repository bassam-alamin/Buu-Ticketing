import uuid
from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class Theater(BaseModel):
    name = models.CharField(max_length=255)
    number_of_seats = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class TheatreSession(BaseModel):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    date = models.DateField()
    name_of_show =models.CharField(max_length=255)
    available_seats = models.JSONField(
        default=list, null=True, blank=True
    )

    def __str__(self):
        return f"{self.theater.name} - {self.date}"


class Reservation(BaseModel):
    seating = models.ForeignKey(TheatreSession, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat_number = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.seating} - Seat {self.seat_number}"
