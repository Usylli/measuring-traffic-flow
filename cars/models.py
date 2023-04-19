from django.db import models

class CarsLocation(models.Model):
    guid = models.CharField(max_length=255)
    datetime = models.DateTimeField()
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    