from django.urls import path


from .views import login, logout, signup, user_list

app_name = 'user'

urlpatterns = [
    path('login/', login.UserLogin.as_view(), name='login'),
    path('logout/', logout.UserLogout.as_view(), name='logout'),
    path('signup/', signup.UserSignup.as_view(), name='signup'),
    path('userlist/', user_list.UserList.as_view(), name='user-list'),
    path('activate/<str:uidb64>/<str:token>/', signup.UserSignupCheck.as_view(), name='signup_check'),
]
