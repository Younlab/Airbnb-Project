import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.files.base import ContentFile

User = get_user_model()


class SettingsBackend:
    def authenticate(self, request, username=None, password=None):
        login_valid = (settings.ADMIN_USERNAME == username)
        password_valid = check_password(password, settings.ADMIN_PASSWORD)

        if login_valid and password_valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(username=username)
                user.is_staff = True
                user.is_superuser = True
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class KakaoBackend:
    def authenticate(self, request, code):

        HEADERS = {
                'Content-Type': "application/x-www-form-urlencoded",
                'Cache-Control': "no-cache",
            }

        def get_access_token(code):
            url = "https://kauth.kakao.com/oauth/token"
            params = {
                'grant_type': 'authorization_code',
                'client_id': settings.KAKAO_APP_ID,
                'redirect_url': 'https://leesoo.kr/members/oauth/',
                'code': code
            }

            response = requests.post(url, params, headers=HEADERS)
            response_dict = response.json()
            access_token = response_dict['access_token']
            return access_token

        def get_user_info(access_token):
            url = "https://kapi.kakao.com/v1/user/me"
            HEADERS.update({'Authorization': "Bearer {}".format(access_token)})
            response = requests.post(url, headers=HEADERS)
            return response.json()

        def create_user_from_kakao_user_info(user_info):
            kakao_id = user_info['id']
            email = user_info['kaccount_email']
            profile_image = user_info['properties']['profile_image']

            user, __ = User.objects.get_or_create(
                username=email,
                defaults={
                    'kakao_id': kakao_id,
                }
            )
            user.profile_image.save(
                'kakao_profile_image.png',
                ContentFile(requests.get(profile_image).content)
            )
            user.activate = True
            user.is_kakao_user = True
            user.save()
            return user

        access_token = get_access_token(code)
        user_info = get_user_info(access_token)
        user = create_user_from_kakao_user_info(user_info)

        return user







