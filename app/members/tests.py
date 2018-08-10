from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


def get_dummy_user():
    user = User.objects.create_user(
        username='dummy_username@test.com',
        first_name='user',
        last_name='test',
        birthday='000000',
        password='test1234',
    )
    user.activate = True
    return user


class UserListTest(APITestCase):
    """
    User List 요청에 관한 테스트
    """
    URL = '/members/userlist/'

    def test_user_list_status_code(self):
        """
        superuser가 아닌 일반 유저일 경우에 요청 결과의 HTTP 상태코드가 403인지 확인
        :return:
        """
        login_user = get_dummy_user()
        print(login_user)
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
