from django.contrib.auth.models import AbstractUser
from django.db import models

from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail

from posts.models import Post


class User(AbstractUser):
    STATUS = (
        ('C', 'Customer'),
        ('H', 'Host'),
    )

    # User Profile Image
    profile_image = ProcessedImageField(
        upload_to='profile_image',
        processors=[Thumbnail(100, 100)],
        format='JPEG',
        options={'quality': 100},
    )

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
