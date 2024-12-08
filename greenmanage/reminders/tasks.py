from celery import shared_task
from .models import Reminders

@shared_task
def budget_overrun(user,category,amount,currency):
    description = f"Вы превысили бюджет в категории {category} на {amount} {currency}!"
    obj = Reminders.objects.create(user=user, description=description)
    obj.save()
    return "Уведомление добавлено!"