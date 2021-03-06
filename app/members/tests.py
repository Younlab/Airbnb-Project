import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from members.tokens import account_activation_token

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
        response = self.client.post(self.URL, data=DUMMY_USER_INFO, format='json', )
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

    def test_user_create_save_db(self):
        """
        user signup 요청 후 실제 DB에 저장되었는지 (모든 필드값이 정상적으로 저장되는지)
        :return:
        """
        response = self.client.post(self.URL, data=DUMMY_USER_INFO, format='json', )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)

        check_fields = [
            'username',
            'first_name',
            'last_name',
            'birthday',
            'password',
        ]
        for field in check_fields:
            self.assertEqual(data[field], DUMMY_USER_INFO[field])


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

    def test_check_user_email_url_status_code_200(self):
        """
        user 회원가입 후 Email Token 인증 url 에서 HTTP 상태코드 201인지 확인
        :return:
        """
        user = get_dummy_user()
        email_auth = {
            'user': user,
            'domain': 'leesoo.kr',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8'),
            'token': account_activation_token.make_token(user)
        }
        URL = f"/members/activate/{email_auth['uid']}/{email_auth['token']}/"
        response = self.client.get(URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

class UserAuthTokenReceiveCheckTest(APITestCase):
    """
    User 회원가입 후 AuthToken 전달 관련된 테스트
    """
    URL = '/members/login/'

    def test_check_user_email_authentication_validation_error(self):
        """
        user 회원가입 후 토큰 인증 확인이 되지않은 이메일로 로그인 할 때, validationError를 발생
        :return:
        """
        # EMAIL 인증하지않은 (user.activate = False)
        user = User.objects.create_django_user(**DUMMY_USER_INFO)
        user.save()

        self.client.post(self.URL, data=LOGIN_USER, format='json',)
        self.assertRaises(ValidationError)

    def test_check_user_email_exist_validation_error(self):
        """
        가입되지 않은 이메일 주소로 토큰 받기를 시도할 때, validationError 발생
        :return:
        """
        self.client.post(self.URL, data=LOGIN_USER, format='json', )
        self.assertRaises(ValidationError)

    def test_user_receive_token_succeed_status_code_200(self):
        """
        user가 토큰 전달받기를 성공하였을 때, HTTP 상태코드 200 인지 확인
        :return:
        """
        get_dummy_user()

        response = self.client.post(self.URL, data=LOGIN_USER, format='json',)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserDeleteTokenTest(APITestCase):
    """
    user (토큰 삭제)로그아웃 테스트
    """
    URL = '/members/logout/'

    def test_user_log_out_status_code_204(self):
        """
        user가 (토큰 삭제)로그아웃시에 HTTP 상태코드가 204인지 확인
        :return:
        """
        get_dummy_user()
        # 테스트 코드 내에서 토큰 받아오기
        response = self.client.post(
            '/members/login/',
            data=LOGIN_USER,
        )

        token = response.json()['token']

        # 테스트 코드 내에서 토큰 인증하기
        # 헤더에 로그인 토큰 올린거임??
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        # self.client.force_authenticate(user)
        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class UserProfileTest(APITestCase):
    """
    User Profile 조회, 수정, 삭제 관련 테스트
    """
    URL = '/members/profile/'

    def setUp(self):
        user = get_dummy_user()
        self.client.force_authenticate(user)

    def test_get_user_profile_status_code_200(self):
        """
        user profile 조회시 성공적으로 HTTP 상태코드가 200인지 확인
        :return:
        """
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_user_profile_status_code_201(self):
        """
        user profile patch(일부 수정) 성공시 HTTP 상태코드가 201인지 확인
        :return:
        """
        patch_user = {
            'birthday': '000001'
        }
        response = self.client.patch(self.URL, data=patch_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_user_profile_save_db(self):
        """
        user profile patch 시에 DB에 저장이 잘 되는지 확인
        :return:
        """
        patch_user = {
            'birthday': '000001'
        }
        response = self.client.patch(self.URL, data=patch_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(data['birthday'], patch_user['birthday'])

    def test_delete_user_profile_status_code_204(self):
        """
        user profile delete 시 HTTP 상태코드가 204인지 확인
        :return:
        """
        response = self.client.delete(self.URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_profile_save_db(self):
        """
        user profile delete 시 DB에 그 정보가 삭제되었는지 확인
        :return:
        """
        self.client.delete(self.URL)
        self.assertIs(User.objects.filter(**DUMMY_USER_INFO).exists(), False)


class UserLikesRoomTest(APITestCase):
    """
    User가 Rooms를 Likes 할 때 관련 테스트
    """
    URL = '/members/likes/'

    def test_user_likes_rooms_status_code_200(self):
        """
        user가 likes한 rooms list를 가져올 때 상태코드 200이 돌아오는지
        :return:
        """
        user = get_dummy_user()
        self.client.force_authenticate(user)

        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserChangePasswordCheckEmailTest(APITestCase):
    """
    User가 Password를 변경할 때 Email 전송 관련 테스트
    """
    URL = '/members/sendemail/'

    def test_user_change_password_check_email_status_code_200(self):
        """
        user가 password 변경에 필요한 uidb64를 알아내기 위해 email을 발송할 때
        정상적으로 HTTP 상태코드가 200으로 돌아오는지
        :return:
        """
        user = get_dummy_user()
        self.client.force_authenticate(user)

        response = self.client.post(
            self.URL,
            data={
                'email': DUMMY_USER_INFO['username'],
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
