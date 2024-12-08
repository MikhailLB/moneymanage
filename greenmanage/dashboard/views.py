from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.shortcuts import render
from .services import sum_amount, spent_amount, budget_remainder
from accounts.models import Account
from budgets.models import Budget
from currencies.models import Currency
from transactions.models import Transaction
from reminders.models import Reminders



@login_required
def main(request):
    curr_code = Account.objects.get(user=request.user).currency.code
    curr_value = Currency.objects.get(code__iexact=curr_code).exchange_rate
    income = sum_amount(request.user, curr_code=curr_code, curr_rate=curr_value)
    expense = spent_amount(request.user, curr_code=curr_code, curr_rate=curr_value)
    budget = budget_remainder(request.user)

    if not Account.objects.get(user_id=request.user.id):
        account = Account.objects.create(user_id=request.user.id, name=request.user.first_name)

    return render(request, 'dashboard/index.html', {'income':income ,'curr_code':curr_code, 'expense':expense, 'budget':budget})