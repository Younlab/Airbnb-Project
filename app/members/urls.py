from django.urls import path


from .views import login, logout, signup, user_list, \
    modify, email_check, likes_rooms, change_password, change_password_check_password, \
    kakao_login

app_name = 'user'

urlpatterns = [
    path('login/', login.UserLogin.as_view(), name='login'),
    path('oauth/', kakao_login.KakaoAuth.as_view(), name='kakao-login'),
    path('facebooklogin/', login.FacebookUserLogin.as_view(), name='facebook-login'),
    path('logout/', logout.UserLogout.as_view(), name='logout'),
    path('emailcheck/', email_check.UserEmailCheck.as_view(), name='email_check'),
    path('sendemail/', change_password_check_password.ChangePasswordCheckEmail.as_view(), name='password-email'),
    path('signup/', signup.UserSignup.as_view(), name='signup'),
    path('userlist/', user_list.UserList.as_view(), name='user-list'),
    path('profile/', modify.UserProfileModified.as_view(), name='user-profile'),
    path('likes/', likes_rooms.UserLikesRooms.as_view(), name='likes-rooms'),
    path('activate/<str:uidb64>/<str:token>/', signup.UserSignupCheck.as_view(), name='signup_check'),
    path('check/<str:uidb64>/', change_password.ChangePassword.as_view(), name='password_check'),
]
