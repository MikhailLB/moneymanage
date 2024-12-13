from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .services import sum_amount, spent_amount, budget_remainder
from accounts.models import Account
from currencies.models import Currency



@login_required
def main(request):
    curr_code = Account.objects.get(user_id=request.user.id).currency.code
    curr_value = Currency.objects.get(code__iexact=curr_code).exchange_rate
    income = sum_amount(request.user, curr_code=curr_code, curr_rate=curr_value)
    expense = spent_amount(request.user, curr_code=curr_code, curr_rate=curr_value)
    budget = budget_remainder(request.user)

    return render(request, 'dashboard/index.html', {'income':income ,'curr_code':curr_code, 'expense':expense, 'budget':budget})