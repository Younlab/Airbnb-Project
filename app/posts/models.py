from django.conf import settings
from django.db import models

from rooms.models import Room


class Post(models.Model):
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL(),
        null=True,
        blank=True,
    )

    title = models.CharField(max_length=200)
    sub_title = models.CharField(max_length=250, blank=True)

    tag = models.CharField(max_length=200, blank=True)


class PostDetail(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )

    room_info = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
    )

    refund = models.CharField(max_length=300)
    reservation = models.CharField(max_length=50)
