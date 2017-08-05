from django.db import models

# Create your models here.
class PerformanceDate(models.Model):
    datum = models.DateField()
    hasFreeSeats = models.BooleanField(default = True)
