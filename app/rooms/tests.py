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


class RoomListTest(APITestCase):
    """
    Rooms List 관련 테스트
    """
    URL = '/rooms/list/'

    def setUp(self):
        user = get_dummy_user()
        self.client.force_authenticate(user)

    def test_get_rooms_list_status_code_200(self):
        """
        Room List 불러올 때 HTTP 상태 코드가 200인지
        :return:
        """
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
