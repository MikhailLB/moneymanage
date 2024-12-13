from locale import currency

from celery import shared_task

from accounts.models import Account
from dashboard.services import budget_remainder
from .models import Reminders

@shared_task
def budget_overrun(user,category,limit, spent, id):
    if not Reminders.objects.filter(budget_id=id).exists():
        currency = Account.objects.get(user=user).currency.code
        exchange_rate = Account.objects.get(user=user).currency.exchange_rate
        amount = limit - spent
        description = f"Вы превысили бюджет в категории {str(category).lower()} на {round(amount * exchange_rate, 2) } {currency}!"
        obj = Reminders.objects.create(user=user, description=description, is_completed=False, budget_id=id)
        obj.save()
        return "Уведомление об превышении бюджета добавлено!"


@shared_task
def regular_pay_notification(user, category, amount, currency):
    description = f"Регулярная транзакция в категории '{str(category).lower()}' суммой {amount} {currency} успешно добавлена! "
    obj = Reminders.objects.create(user=user, description=description, is_completed=False)
    obj.save()
    return "Уведомление регулярном платеже добавлено!"

@shared_task
def change_password_notification(user):
    description = f"Вы успешно сменили пароль!"
    obj = Reminders.objects.create(user=user, description=description, is_completed=False)
    obj.save()

@shared_task
def forgot_password_notification(user):
    description = f"Вы успешно восстановили пароль!"
    obj = Reminders.objects.create(user=user, description=description, is_completed=False)
    obj.save()

@shared_task
def download_statistics(user):
    description = f"Таблица транзакций скачана в формате excel!"
    obj = Reminders.objects.create(user=user, description=description, is_completed=False)
    obj.save()