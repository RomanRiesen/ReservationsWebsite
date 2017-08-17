from django.db import models

# Create your models here.
#FIXME TODO when PerformanceDate is changed, adjust the reservations!!!
#FIXME TODO when PerformanceDate is deleted, delete the reservations!!!
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
    #FIXME add action to change a users date of reservation
    actions = []
