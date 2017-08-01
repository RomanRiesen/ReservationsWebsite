from django.db import models

# Create your models here.
class PerformanceDate(models.Model):
    datum = models.DateField()
    noMoreFreeSeats = models.BooleanField()
