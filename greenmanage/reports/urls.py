from django.contrib import admin
from django.urls import path, include
from .views import *
urlpatterns = [
    path('reports/', expenses_by_day, name='reports')
]