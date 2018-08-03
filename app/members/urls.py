from django.urls import path


from .views import login,logout,signup

app_name = 'user'

urlpatterns = [
    path('login/', login.UserLogin.as_view(), name='login'),
    path('logout/', logout.UserLogout.as_view(), name='logout'),
    path('signup/', signup.UserSignup.as_view(), name='signup'),
    path('activate/<str:uidb64>/<str:token>/', signup.UserSignupCheck.as_view(), name='signup_check'),
]
