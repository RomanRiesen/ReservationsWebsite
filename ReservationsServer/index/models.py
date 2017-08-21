from django.db import models


# Create your models here.
#FIXME TODO when PerformanceDate is changed, adjust the reservations!!!
class PerformanceDate(models.Model):
    datum = models.DateField()
    has_free_seats = models.BooleanField(default = True)
    def __str__(obj):#FIXME format this nicer!
        return str(obj.datum)


#Holds all the reservations
class Reservation(models.Model):
    datum = models.ForeignKey(PerformanceDate, on_delete=models.CASCADE)#FIXME dissalow selection fo empty PerformanceDate
    seatName = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)

    reservation_time = models.TimeField(auto_now_add = True)
    reservation_confirmed = models.BooleanField(default=False)
    reservation_hash = models.CharField(max_length = 255, default = "", editable=False)
    #FIXME add action to change a users date of reservation
    actions = []
