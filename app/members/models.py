from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models

from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail

from rooms.models import Rooms


class UserManager(DjangoUserManager):
    pass


class User(AbstractUser):

    # User Profile Image
    profile_image = ProcessedImageField(
        upload_to='profile_image',
        processors=[Thumbnail(100, 100)],
        format='JPEG',
        options={'quality': 100},
        blank=True,
    )


    # Phone Number
    phone_number = models.CharField(max_length=50)

    # Birthday
    birthday = models.CharField(max_length=100)

    # Email field
    email = models.EmailField()

    # facebook 가입자는 자동으로 True 표시 되게끔 구현하기
    is_facebook_user = models.BooleanField(default=False)

    # 자신이 호스트일 경우 True
    is_host = models.BooleanField(default=False)
    activate = models.BooleanField(default=False)

    likes_posts = models.ManyToManyField(
        Rooms,
        # blank=True,
        related_name='like_posts',
        related_query_name='like_posts',
    )

    # UserManager 동작 설정
    objects = UserManager()