from celery import shared_task
from datetime import datetime, timedelta, date
from accounts.models import Account
from budgets.models import Category
from transactions.models import Transaction
from .models import TempTransaction


@shared_task
def process_auto_payments():
    transactions = TempTransaction.objects.all()
    today = date.today()

    for transaction in transactions:
        should_process = False
        last_processed = transaction.last_processed if transaction.last_processed else (today - timedelta(days=1))

        if isinstance(last_processed, datetime):
            last_processed = last_processed.date()

        elif transaction.frequency.name == 'daily':
            # Проверка для дневной частоты
            if (today - last_processed).days >= 1:
                should_process = True
        elif transaction.frequency.name == 'weekly':
            # Проверка для недельной частоты
            if (today - last_processed).days >= 7:
                should_process = True
        elif transaction.frequency.name == 'monthly':
            # Проверка для месячной частоты
            if today.month != last_processed.month or today.year != last_processed.year:
                should_process = True
        elif transaction.frequency.name == 'yearly':
            # Проверка для годовой частоты
            if today.year != last_processed.year:
                should_process = True

        if should_process:
            Transaction.objects.create(
                user=transaction.user,
                category=Category.objects.get(name=transaction.category),
                amount=transaction.amount,
                account=Account.objects.get(user=transaction.user),
                description=f"Авто-списание: {transaction.description}",
                transaction_type = transaction.transaction_type,
                currency=transaction.currency
            )
            if transaction.frequency.name == 'daily':
                transaction.target_date = datetime.today() + timedelta(days=1)
            elif transaction.frequency.name == 'weekly':
                transaction.target_date = datetime.today() + timedelta(weeks=1)
            elif transaction.frequency.name == 'monthly':
                transaction.target_date = datetime.today() + timedelta(days=30)
                transaction.save()
            transaction.last_processed = today
        transaction.save()

    return "Successfully add transactions"