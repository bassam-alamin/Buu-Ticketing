from django.contrib import admin
from .models import Theater, TheatreSession, Reservation


# Register your models here.

@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return True

    def has_delete_permission(
            self, request, obj=None
    ):
        return True

    search_fields = ['name',]

    exclude = ()
    date_hierarchy = 'created_at'
    list_display = [
        "name", "number_of_seats", "created_at"
    ]


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return True

    def has_delete_permission(
            self, request, obj=None
    ):
        return True

    search_fields = ['seating_name','user_email']

    exclude = ()
    date_hierarchy = 'created_at'
    list_display = [
        "seating", "user", "seat_number"
    ]

@admin.register(TheatreSession)
class TheatreSessionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return True

    def has_delete_permission(
            self, request, obj=None
    ):
        return True

    search_fields = ['theater_name']

    exclude = ()
    date_hierarchy = 'created_at'
    list_display = [
        "theater", "date"
    ]
