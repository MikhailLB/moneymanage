from django.contrib.auth import get_user_model
from django.db import models

class Reminders(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reminders')
    date = models.DateTimeField()
    description = models.CharField(max_length=1024)
    is_completed = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)