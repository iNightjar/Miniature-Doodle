from django.db import models

# Create your models here.

# Guest - Movie - Reservation


class Movie(models.Model):
    hall = models.CharField(max_length=10)
    movie = models.CharField(max_length=30) # extending max_length to 30
    # date = models.DateField(max_length=10) -- No need for the data column


class Guest(models.Model):
    name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=15)


class Reservation(models.Model):
    guest = models.ForeignKey(
        Guest, related_name='reservation', on_delete=models.CASCADE)
    movie = models.ForeignKey(
        Movie, related_name='reservation', on_delete=models.CASCADE)
