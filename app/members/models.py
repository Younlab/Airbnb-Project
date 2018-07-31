from django.contrib.auth.models import AbstractUser
from django.db import models

from posts.models import Post


class User(AbstractUser):
    STATUS = (
        ('C', 'Customer'),
        ('H', 'Host'),
    )

    email = models.EmailField()
    img = models.ImageField(blank=True)
    phone_number = models.CharField(max_length=50)
    status = models.CharField(
        max_length=1,
        default='C',
        choices=STATUS,
    )
    likes_posts = models.ManyToManyField(
        Post,
        blank=True,
        related_name='like_posts',
        related_query_name='like_posts',
    )
