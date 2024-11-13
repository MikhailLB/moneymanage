from django.contrib.auth.views import PasswordChangeDoneView

from .views import *
from django.urls import path, include

app_name = "users"
urlpatterns = [
    path('login/',LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('password-change/', UserPasswordChange.as_view(), name='password-change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(), name='password-change-done'),
]