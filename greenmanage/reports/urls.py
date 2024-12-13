from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('reports/', reports_view, name='reports'),
    path('reports/export/', export_to_excel, name='export_to_excel'),
]