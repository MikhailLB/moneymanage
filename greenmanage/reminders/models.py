from django.contrib.auth import get_user_model
from django.db import models

from budgets.models import Budget


class Reminders(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reminders')
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=1024)
    is_completed = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='reminders', null=True, blank=True)