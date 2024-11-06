from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, ExpressionWrapper, DecimalField
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, UpdateView

from .models import Budget
#from .forms import AddBudgetForm


class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget
    template_name = 'budgets/budgets.html'
    context_object_name = "budgets"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        # Фильтруем по пользователю
        queryset = queryset.filter(user=self.request.user)

        # Сортировка
        order = self.request.GET.get('order', 'desc')
        sort_by = self.request.GET.get('sort_by')
        if sort_by in ['category', 'spent', 'limit']:
            if order == 'desc':
                queryset = queryset.order_by('-' + sort_by)  # По убыванию
            else:
                queryset = queryset.order_by(sort_by)  # По возрастанию

        # Фильтрация
        category = self.request.GET.get('category')
        spent = self.request.GET.get('spent')
        limit = self.request.GET.get('limit')

        if category:
            queryset = queryset.filter(category__name__icontains=category)
        if spent:
            queryset = queryset.filter(spent=spent)
        if limit:
            queryset = queryset.filter(limit=limit)

        # Добавляем поле remainder
        queryset = queryset.annotate(
            remainder=ExpressionWrapper(F('limit') - F('spent'), output_field=DecimalField())
        )
        return queryset
        #return Budget.objects.all().annotate(remainder=F('limit')+F('spent'))

class UpdateLimit(LoginRequiredMixin, UpdateView):
    model = Budget
    fields = ['limit']
    template_name = 'budgets/update_budget.html'
    success_url = reverse_lazy('budgets')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Фильтруем по пользователю
        data = Budget.objects.filter(user=self.request.user).annotate(
            remainder=ExpressionWrapper(F('limit') - F('spent'), output_field=DecimalField())
        )
        context['budgets'] = data
        context['pk'] = self.kwargs.get('pk')  # Передаем идентификатор текущего бюджета
        return context

class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    model = Budget
    success_url = reverse_lazy('budgets')