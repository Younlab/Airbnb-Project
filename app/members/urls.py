from django.urls import path


from .views import login, logout, signup, user_list, modify, email_check

app_name = 'user'

urlpatterns = [
    path('login/', login.UserLogin.as_view(), name='login'),
    path('facebooklogin/', login.FacebookUserLogin.as_view(), name='facebook-login'),
    path('logout/', logout.UserLogout.as_view(), name='logout'),
    path('emailcheck/', email_check.UserEmailCheck.as_view(), name='email_check'),
    path('signup/', signup.UserSignup.as_view(), name='signup'),
    path('userlist/', user_list.UserList.as_view(), name='user-list'),
    path('profile/', modify.UserProfileModefied.as_view(), name='user-profile'),
    path('activate/<str:uidb64>/<str:token>/', signup.UserSignupCheck.as_view(), name='signup_check'),
]
