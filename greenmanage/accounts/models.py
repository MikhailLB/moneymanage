from django.contrib.auth import get_user_model
from django.db import models
from currencies.models import Currency

class Account(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='account')
    name = models.CharField(max_length=128)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.balance} {self.currency}"