from django.db import models


class Room(models.Model):
    Facilities = models.CharField(max_length=400)
    using_info = models.CharField(max_length=200)
    room_info = models.TextField()
    rule = models.TextField()
    price = models.IntegerField()
    location = models.CharField(max_length=200)
