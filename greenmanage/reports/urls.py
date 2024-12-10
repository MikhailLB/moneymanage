from django.contrib import admin
from django.urls import path, include
from .views import *
urlpatterns = [
    path('reports/', export_to_excel, name='reports')
]