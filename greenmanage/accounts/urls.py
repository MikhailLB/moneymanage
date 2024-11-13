from django.urls import path, include
from .views import *
urlpatterns = [
    path('accounts/', main, name='accounts'),
    path('accounts-update/<int:pk>', UpdateAccountView.as_view(), name='accounts_update')
]