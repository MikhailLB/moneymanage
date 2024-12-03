from django.contrib.auth import get_user_model

from accounts.models import Account
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db import models
from budgets.models import Category, Budget
from decimal import Decimal
class Transaction(models.Model):

    account = models.ForeignKey(Account, on_delete=models.CASCADE, default=1)
    date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=1023)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.ForeignKey('TransactionsType', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.account} {self.category} {self.amount} {self.transaction_type}"

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]


@receiver(post_save, sender=Transaction)
def update_budget_on_transaction(sender, instance, created, **kwargs):
    if created:
        category = instance.category
        amount = instance.amount
        transaction_type = instance.transaction_type
        user_id = instance.user_id

        # Убедимся, что это не доход (income)
        if str(transaction_type) != 'income':
            # Создаем или обновляем бюджет для данной категории и пользователя
            budget, created_budget = Budget.objects.get_or_create(
                category=category,
                user_id=user_id,  # Убедитесь, что бюджет уникален для пользователя
                defaults={'limit': Decimal('100.00'), 'spent': Decimal('0.00')}
            )

            # Обновляем поле spent
            budget.spent += abs(amount)  # Убедитесь, что сумма добавляется как положительная
            budget.save()


@receiver(post_delete, sender=Transaction)
def delete_budget_on_transaction(sender, instance, **kwargs):
    category = instance.category
    amount = instance.amount
    transaction_type = instance.transaction_type
    user_id = instance.user_id

    # Проверяем, существует ли бюджет для данной категории и пользователя
    try:
        budget = Budget.objects.get(category=category, user_id=user_id)

        # Если это не доход (income)
        if str(transaction_type) != 'income':
            # Проверяем, можем ли уменьшить значение spent
            if budget.spent - abs(amount) > 0:
                budget.spent -= abs(amount)
            else:
                budget.spent = 0  # Если сумма уходит в минус, установим в 0
            budget.save()

    except Budget.DoesNotExist:
        pass
class TransactionsType(models.Model):
    name = models.CharField(max_length=255)
    verbose_name = models.CharField(max_length=255)

    def __str__(self):
        return self.verbose_name