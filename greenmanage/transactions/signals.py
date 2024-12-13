from decimal import Decimal

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from budgets.models import Budget
from currencies.models import Currency
from transactions.models import Transaction


@receiver(post_save, sender=Transaction)
def update_budget_on_transaction(sender, instance, created, **kwargs):
    if created:
        category = instance.category
        amount = instance.amount
        transaction_type = instance.transaction_type
        user_id = instance.user_id
        currency = instance.currency

        if str(transaction_type) != 'income':

            budget, created_budget = Budget.objects.get_or_create(
                category=category,
                user_id=user_id,
                defaults={'limit': Decimal('100.00'), 'spent': Decimal('0.00')}
            )

            currency_rate = Currency.objects.get(pk=currency.pk).exchange_rate
            budget.spent += abs(amount / currency_rate)
            budget.save()


@receiver(post_delete, sender=Transaction)
def delete_budget_on_transaction(sender, instance, **kwargs):
    category = instance.category
    amount = instance.amount
    transaction_type = instance.transaction_type
    user_id = instance.user_id
    currency = instance.currency

    try:
        budget = Budget.objects.get(category=category, user_id=user_id)

        if str(transaction_type) != 'income':
            if budget.spent - abs(amount) > 0:
                currency_rate = Currency.objects.get(pk=currency.pk).exchange_rate
                budget.spent -= abs(amount / currency_rate)
            else:
                budget.spent = 0
            budget.save()

    except Budget.DoesNotExist:
        pass