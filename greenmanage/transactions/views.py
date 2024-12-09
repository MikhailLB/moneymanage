from numpy.ma.core import around
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormMixin, DeleteView

from currencies.models import Currency
from .forms import *
from .models import Transaction
class TransactionsListView(LoginRequiredMixin, FormMixin, ListView):
    model = Transaction
    form_class = CreateTransactionForm
    template_name = 'transactions/transactions.html'
    context_object_name = 'transactions'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        order = self.request.GET.get('order', 'desc')  # по умолчанию сортировка по убыванию
        sort_by = self.request.GET.get('sort_by')  # параметр сортировки

        # Проверка, нужно ли сортировать
        if sort_by in ['amount', 'date', 'category', 'transaction_type']:
            if order == 'asc':
                queryset = queryset.order_by(sort_by)  # по возрастанию
            else:
                queryset = queryset.order_by('-' + sort_by)  # по убыванию

        # Фильтрация по категории
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__name__icontains=category)

        # Фильтрация по дате
        date = self.request.GET.get('date')
        if date:
            queryset = queryset.filter(date=date)

        # Фильтрация по типу транзакции
        transaction_type = self.request.GET.get('transaction_type')
        if transaction_type:
            queryset = queryset.filter(transaction_type__name__icontains=transaction_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['category_filter'] = self.request.GET.get('category', '')
        context['date_filter'] = self.request.GET.get('date', '')
        context['transaction_type_filter'] = self.request.GET.get('transaction_type', '')
        context['sort_by'] = self.request.GET.get('sort_by', '')
        context['current_order'] = self.request.GET.get('order', 'desc')
        return context

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()  # передаем данные формы из запроса

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('transactions')

    def get_initial(self):
        initial = super().get_initial()
        initial['user_id'] = self.request.user.id
        return initial
    def form_valid(self, form):
        context = self.get_context_data()

        transaction = form.save(commit=False)

        if transaction.transaction_type.name == 'income':
            transaction.amount = abs(transaction.amount)
        elif transaction.transaction_type.name == 'expense':
            transaction.amount = -abs(transaction.amount)

        transaction.user = self.request.user
        transaction.save()

        return super().form_valid(form)


class DeleteTransactionView(LoginRequiredMixin, DeleteView):
    model = Transaction
    success_url = reverse_lazy('transactions')