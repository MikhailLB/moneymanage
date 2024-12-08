from budgets.models import Budget
from transactions.models import Transaction


def sum_amount(user, curr_code, curr_rate):
    transactions = Transaction.objects.filter(user=user, transaction_type__name='income')
    amount = 0
    for transaction in transactions:
        if transaction.currency != curr_code:
            transaction.amount = transaction.amount * curr_rate
            amount += transaction.amount
        else:
            amount += transaction.amount
    return round(amount, 2)

def spent_amount(user, curr_code, curr_rate):
    transactions = Transaction.objects.filter(user=user, transaction_type__name='expense')
    expense = 0
    for transaction in transactions:
        if transaction.currency != curr_code:
            transaction.amount = transaction.amount * curr_rate
            expense += transaction.amount
        else:
            expense += transaction.amount
    return round(expense, 2)

def budget_remainder(user):
    budgets = Budget.objects.filter(user=user)
    limit = 0
    spent = 0
    for budget in budgets:
        spent += budget.spent
        limit += budget.limit
    return round(limit - spent, 2)