from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()

user = {
    'username': 'dummy_username@test.com',
    'first_name': 'user',
    'last_name': 'test',
    'birthday': '000000',
    'password': 'test1234'
}


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

    def test_not_admin_status_code_403(self):
        """
        superuser가 아닌 일반 유저일 경우에 요청 결과의 HTTP 상태코드가 403인지 확인
        :return:
        """
        # user 회원가입 시키기 & 이메일 인증 True로 바꾸고 저장
        login_user = User.objects.create_django_user(**user)
        login_user.activate = True
        login_user.save()

        # 로그인을 그냥 바로 시켜버림!
        self.client.force_authenticate(login_user)

        response = self.client.get(self.URL)
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
