from tkinter.font import names

from django.contrib.auth import get_user_model
from django.db import models
from currencies.models import Currency
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
class Account(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='account')
    name = models.CharField(max_length=128)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.balance} {self.currency}"

    @receiver(post_save, sender=get_user_model())
    def create_account(sender, instance, created, **kwargs):
        if created:
            first_name = instance.first_name
            acc = Account.objects.create(user=instance, name=first_name)
            acc.save()
