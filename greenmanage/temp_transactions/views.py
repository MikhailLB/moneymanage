from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ExpressionWrapper, F, DateField, DurationField
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from temp_transactions.form import TempTransactionForm
from temp_transactions.models import TempTransaction


class CreateTempTransaction(LoginRequiredMixin, CreateView):
    model = TempTransaction
    form_class = TempTransactionForm
    template_name = 'temp_transactions/temp_transactions.html'
    success_url = reverse_lazy('temp_transactions_list')

    def get_initial(self):
        initial = super().get_initial()
        initial['user_id'] = self.request.user.id
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ListTempTransaction(LoginRequiredMixin, ListView):
    model = TempTransaction
    template_name = 'temp_transactions/temp_transactions_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        query_set = super().get_queryset()
        query_set = query_set.filter(user=self.request.user).annotate(
            rest=F('target_date') - datetime.today().date()
        )
        return query_set

class TempTransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = TempTransaction
    success_url = reverse_lazy('temp_transactions_list')

class TempTransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = TempTransaction
    template_name = 'temp_transactions/temp_transaction_update.html'
    success_url = reverse_lazy('temp_transactions_list')
    fields = ['category','description', 'transaction_type', 'amount','currency']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_set = TempTransaction.objects.filter(pk=self.kwargs['pk']).annotate(
            rest=F('target_date') - datetime.today().date()
        )

        # Получаем rest для первой (или единственной) транзакции
        if query_set.exists():
            transaction = query_set.first()
            context['rest'] = transaction.rest  # добавляем поле rest в контекст
        context['transaction'] = get_object_or_404(TempTransaction, pk=self.kwargs['pk'])
        return context
