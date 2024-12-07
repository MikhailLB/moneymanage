from django.contrib import admin
from django.urls import path, include
from .views import *
urlpatterns = [
    path('temp/transactions/', CreateTempTransaction.as_view(), name='temp_transactions'),
]