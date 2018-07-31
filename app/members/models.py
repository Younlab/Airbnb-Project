from django.contrib.auth.models import AbstractUser
from django.db import models

from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail

from posts.models import Post


class User(AbstractUser):

    # User Profile Image
    profile_image = ProcessedImageField(
        upload_to='profile_image',
        processors=[Thumbnail(100, 100)],
        format='JPEG',
        options={'quality': 100},
    )

    # Phone Number
    phone_number = models.CharField(max_length=50)

    # Email field
    email = models.EmailField()

    # facebook 가입자는 자동으로 True 표시 되게끔 구현하기
    is_facebook_user = models.BooleanField(default=False)

    # 자신이 호스트일 경우 True
    is_host = models.BooleanField(default=False)

    # User type
    likes_posts = models.ManyToManyField(
        Post,
        blank=True,
        related_name='like_posts',
        related_query_name='like_posts',
    )
