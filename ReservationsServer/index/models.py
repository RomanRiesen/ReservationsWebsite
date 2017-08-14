from django.db import models

# Create your models here.
class PerformanceDate(models.Model):
    datum = models.DateField()
    has_free_seats = models.BooleanField(default = True)


#Holds all the reservations
class Reservation(models.Model):
    #TODO make this foreign field
    datum = models.DateField()
    seatName = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    reservation_time = models.TimeField(auto_now_add = True)
