from django.urls import path

from .views import login,signup

urlpatterns = [
    path('login/', login.UserLogin.as_view(), name='login'),
    path('signup/', signup.UserSignup.as_view(), name='signup'),
]
