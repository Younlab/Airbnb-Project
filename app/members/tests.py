from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from members.tokens import account_activation_token

User = get_user_model()


NOT_SIGNUP_DUMMY_USER = {
        'username': 'dummy_username@test.com',
        'first_name': 'user',
        'last_name': 'test',
        'birthday': '000000',
        'password': 'test1234',
    }

LOGIN_USER = {
            'username': NOT_SIGNUP_DUMMY_USER['username'],
            'password': NOT_SIGNUP_DUMMY_USER['password'],
        }


# user 회원가입 시키기 & 이메일 인증 True로 바꾸고 저장
def get_dummy_user():
    user = User.objects.create_django_user(**NOT_SIGNUP_DUMMY_USER)
    user.activate = True
    user.save()
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
        user = get_dummy_user()
        # 로그인을 그냥 바로 시켜버림!
        self.client.force_authenticate(user)

        response = self.client.get(self.URL)
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserSignUpTest(APITestCase):
    """
    User SignUp 에 관한 테스트
    """
    URL = '/members/signup/'

    def test_user_sign_up_succeed_status_code_201(self):
        """
        user 회원가입 정보가 정상적으로 요청되었을 때 요청 결과의 HTTP 상태코드가 201인지 확인
        json으로 요청하고 201 상태코드를 받아옴
        :return:
        """
        response = self.client.post(self.URL, data=NOT_SIGNUP_DUMMY_USER, format='json', )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_sign_up_wrong_password_occurred_validation_error(self):
        """
        user 회원가입 중 Password가 8자리가 안될 경우, ValidationError 발생
        :return:
        """
        # 비밀번호가 7자리인 user
        user = {
            'username': 'dummy_username@test.com',
            'first_name': 'user',
            'last_name': 'test',
            'birthday': '000000',
            'password': 'test123'
        }
        self.client.post(self.URL, data=user, format='json',)
        self.assertRaises(ValidationError)


class UserEmailActivateCheckTest(APITestCase):
    """
    User SignUp 시에 Email 인증 관련 테스트
    """

    def test_check_user_email_token_equal(self):
        """
        user 회원가입 후 발송되는 인증 확인 이메일 token값과 DB에 저장되는 이메일 token 값이 같은지 확인
        :return:
        """
        user = get_dummy_user()

        # user email token 값과 DB상의 토큰 값 비교
        token = account_activation_token.make_token(user)
        self.assertTrue(account_activation_token.check_token(user, token))


class UserLoginTest(APITestCase):
    """
    User Login 시에 관련된 테스트
    """
    URL = '/members/login/'

    def test_check_user_email_authentication_validation_error(self):
        """
        user 회원가입 후 인증 확인이 되지않은 이메일로 로그인 할 때, validationError를 발생
        :return:
        """
        # EMAIL 인증하지않은 (user.activate = False)
        user = User.objects.create_django_user(**NOT_SIGNUP_DUMMY_USER)
        user.save()

        self.client.post(self.URL, data=LOGIN_USER, format='json',)
        self.assertRaises(ValidationError)

    def test_check_user_email_exist_validation_error(self):
        """
        가입되지 않은 이메일 주소로 로그인을 할때, validationError 발생
        :return:
        """
        self.client.post(self.URL, data=LOGIN_USER, format='json', )
        self.assertRaises(ValidationError)
