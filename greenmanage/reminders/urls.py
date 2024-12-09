from django.contrib import admin
from django.urls import path, include
from .views import *
urlpatterns = [
    path('reminders/', NotificationsListView.as_view(), name='reminders'),
    path('reminders/delete/<int:pk>', delete_reminder, name='reminders-delete'),
]