from django.urls import path, include
from .views import *
urlpatterns = [
    path('accounts/', main, name='accounts')
]