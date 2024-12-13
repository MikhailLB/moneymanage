from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('transactions/', TransactionsListView.as_view(), name='transactions'),
    path('delete-transaction/<int:pk>', DeleteTransactionView.as_view(), name='delete_transaction')
]