from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.booking.models import Reservation



@receiver(post_save, sender=Reservation)
def handle_reservation_post_save(sender, instance, **kwargs):
    seating = instance.seating
    if seating:
        seating.available_seats.remove(
            instance.seat_number
        )
        seating.save()