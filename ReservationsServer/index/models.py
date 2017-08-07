from django.db import models

# Create your models here.
class PerformanceDate(models.Model):
    datum = models.DateField()
    has_free_seats = models.BooleanField(default = True)
