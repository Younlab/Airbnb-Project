from django.urls import path


from .views import *

app_name = 'user'

urlpatterns = [
    path('login/', auth.UserAuth.as_view(), name='auth'),
    path('oauth/', kakao_auth.KakaoAuth.as_view(), name='kakao-auth'),
    path('facebooklogin/', auth.FacebookUserAuth.as_view(), name='facebook-auth'),
    path('logout/', delete_auth.DeleteUserAuth.as_view(), name='delete-auth'),
    path('emailcheck/', email_check.UserEmailCheck.as_view(), name='email-check'),
    path('sendemail/', change_password_check_password.ChangePasswordCheckEmail.as_view(), name='password-email'),
    path('signup/', signup.UserSignup.as_view(), name='signup'),
    path('userlist/', user_list.UserList.as_view(), name='user-list'),
    path('profile/', modify.UserProfileModified.as_view(), name='user-profile'),
    path('likes/', likes_rooms.UserLikesRooms.as_view(), name='likes-rooms'),
    path('activate/<str:uidb64>/<str:token>/', signup.UserSignupCheck.as_view(), name='signup-check'),
    path('check/<str:uidb64>/', change_password.ChangePassword.as_view(), name='password-check'),
]
