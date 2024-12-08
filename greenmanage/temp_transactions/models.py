from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.db import models

from currencies.models import Currency
from transactions.models import TransactionsType


class TempTransaction(models.Model):
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    last_processed = models.DateField(null=True, blank=True)
    frequency = models.ForeignKey('Frequency', on_delete=models.SET_NULL, null=True)
    category = models.CharField(max_length=50)
    transaction_type = models.ForeignKey(TransactionsType, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    target_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.category} {self.description} {self.amount} {self.currency}'



class Frequency(models.Model):
    name = models.CharField(max_length=10, unique=True)
    rus_name = models.CharField(max_length=10, unique=True)
    frequency = models.IntegerField()

    def __str__(self):
        return self.name