from django.contrib import admin

# Register your models here.
from .models import PerformanceDate

@admin.register(PerformanceDate)
class PerformanceDateAdmin(admin.ModelAdmin):
    list_display = ('datum', 'hasFreeSeats')
    ordering = ('datum', 'hasFreeSeats', 'id')
    def datum(self, obj):
        return obj.datum

    datum.admin_order_field = 'datum'
