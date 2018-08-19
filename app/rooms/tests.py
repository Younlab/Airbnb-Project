from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()

DUMMY_USER_INFO = {
        'username': 'dummy_username@test.com',
        'first_name': 'user',
        'last_name': 'test',
        'birthday': '000000',
        'password': 'test1234',
    }

LOGIN_USER = {
        'username': DUMMY_USER_INFO['username'],
        'password': DUMMY_USER_INFO['password'],
    }


# user 회원가입 시키기 & 이메일 인증 True로 바꾸고 저장
def get_dummy_user():
    try:
        user = User.objects.get(**DUMMY_USER_INFO)
        return user
    except User.DoesNotExist:
        user = User.objects.create_django_user(**DUMMY_USER_INFO)
        user.activate = True
        user.save()
        return user

