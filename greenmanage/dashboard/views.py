from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.shortcuts import render
from budgets.models import Budget
from transactions.models import Transaction
from reminders.models import Reminders

@login_required
def main(request):
    spent_filter = Budget.objects.filter(user=request.user)
    spent = spent_filter.aggregate(Sum('spent'))
    income_filter = Transaction.objects.filter(user=request.user, amount__gt=0)
    income = income_filter.aggregate(Sum('amount'))
    last_budget_filter = Budget.objects.filter(user=request.user).annotate(remainder=F('limit') - F('spent'))
    last_budget = last_budget_filter.aggregate(Sum('remainder'))
    unread_notifications = Reminders.objects.filter(user=request.user, is_completed=False).count()
    if income['amount__sum'] == None:
         income['amount__sum'] = 0
    if last_budget['remainder__sum'] == None:
        last_budget['remainder__sum'] = 0
    if spent['spent__sum'] == None:
        spent['spent__sum'] = 0
    return render(request, 'dashboard/index.html', {'spent':spent, 'income':income, 'last_budget':last_budget, 'unread_notifications':unread_notifications})