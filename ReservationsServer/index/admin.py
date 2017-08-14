from django.contrib import admin

# Register your models here.
from .models import PerformanceDate, Reservation

#https://stackoverflow.com/questions/4938491/django-admin-change-header-django-administration-text

@admin.register(PerformanceDate)
class PerformanceDateAdmin(admin.ModelAdmin):
    list_display = ('datum', 'has_free_seats')
    ordering = ('datum', 'has_free_seats', 'id')
    def datum(self, obj):
        return obj.datum

    datum.admin_order_field = 'datum'


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('datum', 'email', 'seatName', 'reservation_time')
    ordering = ('datum',)
