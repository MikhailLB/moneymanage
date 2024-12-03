from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth import get_user_model
from accounts.models import Account, Currency


class UpdateProfileForm(forms.ModelForm):
    username = forms.CharField(disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    currency = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'currency']
        labels = {'username': 'Имя пользователя', 'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'E-mail',
                  'currency': 'Валюта'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Загружаем валюты из модели Currency
        self.fields['currency'].choices = [(currency.pk, currency.code) for currency in Currency.objects.all()]

        # Проверка, что у пользователя есть account, и установка начального значения для currency
        if hasattr(self.instance, 'account') and self.instance.account:
            self.fields['currency'].initial = self.instance.account.currency_id

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError("E-mail already exists")
        return email

    def save(self, commit=True):
        user = super().save(commit=commit)
        if not hasattr(user, 'account') or user.account is None:
            raise ValidationError("Account profile does not exist for this user.")

        # Обновляем currency в существующем account

        currency_code = self.cleaned_data['currency']
        user.account.currency = Currency.objects.get(pk=currency_code)

        if commit:
            user.account.save()

        return user
