from datetime import datetime, timedelta, date

from django.forms import ModelForm, TextInput, Select
from django import forms

from accounts.models import Account
from budgets.models import Category
from temp_transactions.models import TempTransaction, Frequency


class TempTransactionForm(ModelForm):
    new_category = forms.CharField(max_length=100, required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = TempTransaction

        fields = ['description', 'frequency', 'new_category', 'transaction_type', 'currency', 'amount']

        widgets = {
            'description': TextInput(attrs={'class': 'form-control'}),
            'new_category': TextInput(attrs={'class': 'form-control'}),
            'amount': TextInput(attrs={'class': 'form-control'}),
            'transaction_type': Select(attrs={'class': 'form-control'}),  # Виджет для выбора типа транзакции
            'currency': Select(attrs={'class': 'form-control'}),  # Виджет для выбора валюты
            'frequency': Select(attrs={'class': 'form-control'}),  # Виджет для выбора частоты
        }

        labels = {
            'description': 'Описание',
            'frequency': 'Переодичность снятия/зачисления средств',
            'new_category': 'Категория',
            'transaction_type': 'Тип транзакции',
            'currency': 'Валюта',
            'amount': 'Сумма',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user = self.initial.get('user_id')
        account = Account.objects.get(user=user)
        self.fields['currency'].initial = account.currency_id
        self.fields['frequency'].choices = [(frequency.pk, frequency.rus_name) for frequency in Frequency.objects.all()]
        self.fields['frequency'].initial = 1

    def save(self, commit=True):
        transaction = super().save(commit=False)
        new_category_name = self.cleaned_data.get('new_category')
        if new_category_name:
            category, created = Category.objects.get_or_create(name=new_category_name)
            transaction.category = category

        if transaction.frequency.name == 'daily':
            transaction.target_date = datetime.today() + timedelta(days=1)

        elif transaction.frequency.name == 'weekly':
            transaction.target_date = datetime.today() + timedelta(weeks=1)

        elif transaction.frequency.name == 'monthly':
            transaction.target_date = datetime.today() + timedelta(days=30)
            transaction.save()

        if commit:
            transaction.save()

        return transaction