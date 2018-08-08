from django.urls import path


from .views import login, logout, signup, user_list, modify

app_name = 'user'

urlpatterns = [
    path('login/', login.UserLogin.as_view(), name='login'),
    path('logout/', logout.UserLogout.as_view(), name='logout'),
    path('signup/', signup.UserSignup.as_view(), name='signup'),
    path('userlist/', user_list.UserList.as_view(), name='user-list'),
    path('profile/', modify.UserProfileModefied.as_view(), name='user-profile'),
    path('activate/<str:uidb64>/<str:token>/', signup.UserSignupCheck.as_view(), name='signup_check'),
]
