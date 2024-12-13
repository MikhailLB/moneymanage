from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Account
from budgets.models import Budget
from reminders.tasks import budget_overrun


@receiver(post_save, sender=Budget)
def budget_post_save(sender, instance, created, **kwargs):
    spent = round(instance.spent / Account.objects.get(user=instance.user).currency.exchange_rate, 2)

    if not created:
        if instance.limit < spent:
            budget_overrun(user=instance.user, category=instance.category, limit=instance.limit, spent=spent,
                       id=instance.pk)
