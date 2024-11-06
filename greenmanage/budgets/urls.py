from django.contrib import admin
from django.urls import path, include
from .views import *



urlpatterns = [
    path('budgets/', BudgetListView.as_view(), name='budgets'),
    path('delete-budget/<int:pk>', BudgetDeleteView.as_view(), name='delete_budget'),
    path('update-budget/<int:pk>', UpdateLimit.as_view(), name='update_limit'),

]