from django.db import models


# Create your models here.


class Room(models.Model):
    Facilities = models.CharField(max_length=400)
    using_info = models.CharField(max_length=200)
    room_info = models.TextField()
    rule = models.CharField(max_length=200)
    price = models.IntegerField()
    location = models.CharField(max_length=200)
