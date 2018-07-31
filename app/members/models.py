from django.contrib.auth.models import AbstractUser
from django.db import models

from posts.models import Post


class User(AbstractUser):
    STATUS = (
        ('C', 'Customer'),
        ('H', 'Host'),
    )


    # User ID
    username = models.CharField(unique=True)
    # User Profile Image
    profile_image = models.ImageField(blank=True, upload_to='user_profile_image')
    # Phone Number
    phone_number = models.CharField(max_length=50)
    status = models.CharField(
        max_length=1,
        choices=STATUS,
    )
    # User type
    likes_posts = models.ManyToManyField(
        Post,
        blank=True,
        related_name='like_posts',
        related_query_name='like_posts',
    )
