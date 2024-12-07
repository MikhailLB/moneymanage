from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from temp_transactions.form import TempTransactionForm
from temp_transactions.models import TempTransaction


class CreateTempTransaction(CreateView):
    model = TempTransaction
    form_class = TempTransactionForm
    template_name = 'temp_transactions/temp_transactions.html'
    success_url = reverse_lazy('transactions')

    def get_initial(self):
        initial = super().get_initial()
        initial['user_id'] = self.request.user.id  # Передаём user_id в начальные данные
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user  # Привязываем пользователя
        return super().form_valid(form)