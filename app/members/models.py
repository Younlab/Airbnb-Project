from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models

from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail

from rooms.models import Rooms


class UserManager(DjangoUserManager):
    def create_django_user(self, *args, **kwargs):
        user = User.objects.create_user(
            username=kwargs.get('username'),
            email=kwargs.get('email'),
            password=kwargs.get('password'),
            first_name=kwargs.get('first_name', ''),
            phone_number=kwargs.get('phone_number', ''),
        )
        return user


class User(AbstractUser):

    GENDER_CHOICE = (
        ('N', 'Nothing'),
        ('F', 'Female'),
        ('M', 'Male'),
    )

    # User Profile Image
    profile_image = ProcessedImageField(
        upload_to='profile_image',
        processors=[Thumbnail(100, 100)],
        format='png',
        options={'quality': 100},
        blank=True,
    )


    # Phone Number
    phone_number = models.CharField(max_length=50, blank=True)

    # Birthday
    birthday = models.CharField(max_length=100, blank=True)

    # Email field
    username = models.EmailField(unique=True, verbose_name='이메일', blank=True)

    # Name field
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)

    # facebook 가입자는 자동으로 True 표시 되게끔 구현하기
    facebook_id = models.CharField(max_length=200, blank=True)
    is_facebook_user = models.BooleanField(default=False)

    # 자신이 호스트일 경우 True
    is_host = models.BooleanField(default=False)
    activate = models.BooleanField(default=False)

    gender = models.CharField(max_length=1, choices=GENDER_CHOICE, default='N')

    # 회원가입 날짜
    create_date = models.DateField(auto_now_add=True)

    likes_posts = models.ManyToManyField(
        Rooms,
        # blank=True,
        related_name='like_posts',
        related_query_name='like_posts',
    )

    # UserManager 동작 설정
    objects = UserManager()
