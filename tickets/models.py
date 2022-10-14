from django.db import models

# Token model to generate token key for every guest(user) gets created
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings



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




# autogenerate tokens for newusers
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def TokenCreate(sender, instance, created, **Kwargs):
    if created:
        Token.objects.create(user=instance)