from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, ExpressionWrapper, DecimalField
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, UpdateView

from reminders.tasks import budget_overrun
from accounts.models import Account
from currencies.models import Currency
from .models import Budget


class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget
    template_name = 'budgets/budgets.html'
    context_object_name = "budgets"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(user=self.request.user)

        order = self.request.GET.get('order', 'desc')
        sort_by = self.request.GET.get('sort_by')

        if sort_by in ['category', 'spent', 'limit']:
            if order == 'desc':
                queryset = queryset.order_by('-' + sort_by)
            else:
                queryset = queryset.order_by(sort_by)

        category = self.request.GET.get('category')
        spent = self.request.GET.get('spent')
        limit = self.request.GET.get('limit')

        if category:
            queryset = queryset.filter(category__name__icontains=category)

        if spent:
            queryset = queryset.filter(spent=spent)

        if limit:
            queryset = queryset.filter(limit=limit)

        queryset = queryset.annotate(
            remainder=ExpressionWrapper((F('limit') - F('spent')), output_field=DecimalField())
        )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['curr_code'] = Account.objects.get(user=self.request.user).currency.code
        context['curr_value'] = Currency.objects.get(code__iexact=context['curr_code']).exchange_rate

        return context

class UpdateLimit(LoginRequiredMixin, UpdateView):
    model = Budget
    fields = ['limit']
    template_name = 'budgets/update_budget.html'
    success_url = reverse_lazy('budgets')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        data = Budget.objects.filter(user=self.request.user).annotate(
            remainder=ExpressionWrapper(F('limit') - F('spent'), output_field=DecimalField())
        )

        context['budgets'] = data
        context['pk'] = self.kwargs.get('pk')
        context['curr_code'] = Account.objects.get(user=self.request.user).currency.code
        context['curr_value'] = Currency.objects.get(code__iexact=context['curr_code']).exchange_rate

        return context

class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    model = Budget
    success_url = reverse_lazy('budgets')