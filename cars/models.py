from django.db import models

class CarsLocation(models.Model):
    guid = models.CharField(max_length=255)
    datetime = models.DateTimeField()
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)

class Incidents(models.Model):
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    datetime = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=255)