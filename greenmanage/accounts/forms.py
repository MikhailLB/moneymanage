from django import forms
from django.db.backends.utils import format_number


class ProfileForm(forms.ModelForm):
    username = forms.CharField(disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField( widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        fields = ['username', 'name', 'last_name', 'email']
        labels = {'username': 'Имя пользователя', 'name': 'Имя', 'last_name': 'Фамилия', 'email': 'E-mail'}