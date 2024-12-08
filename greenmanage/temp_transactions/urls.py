from django.contrib import admin
from django.urls import path, include
from .views import *
urlpatterns = [
    path('temp/transactions/', CreateTempTransaction.as_view(), name='temp_transactions'),
    path('temp/transactions/list', ListTempTransaction.as_view(), name='temp_transactions_list'),
    path('temp/transactions/delete-transaction/<int:pk>', TempTransactionDeleteView.as_view(), name='delete_temp_transaction'),
    path('temp/transactions/update-transaction/<int:pk>', TempTransactionUpdateView.as_view(), name='update_temp_transaction')
]