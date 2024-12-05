from django import forms
from .models import Transaction, Category, TransactionsType  # убедись, что импортируешь нужные модели

class CreateTransactionForm(forms.ModelForm):
    new_category = forms.CharField(max_length=100, required=False)
    class Meta:
        model = Transaction
        fields = ['new_category', 'description', 'transaction_type', 'amount', 'currency']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['currency'].initial = self.instance.account.currency_id

    def save(self, commit=True):
        transaction = super().save(commit=False)
        new_category_name = self.cleaned_data.get('new_category')
        if new_category_name:
            category, created = Category.objects.get_or_create(name=new_category_name)
            transaction.category = category

        if commit:
            transaction.save()
        return transaction
