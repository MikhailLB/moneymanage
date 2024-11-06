from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль')

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    password1 = forms.CharField(label='Пароль')
    password2 = forms.CharField(label='Повтор пароля')

    class Meta:
        model = get_user_model()
        fields = ['username','first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {"username": "Логин",
                  "first_name": "Имя",
                  "last_name": "Фамилия",
                  "email": "E-mail",
                  "password1": "Пароль"}
    # def clean_password2(self):
    #     cd = self.cleaned_data
    #     if cd['password1'] != cd["password2"]:
    #         raise forms.ValidationError("Пароли не совпадают!")
    #     else:
    #         return cd['password1']

    def clean_email(self):
        cd = self.cleaned_data['email']
        if get_user_model().objects.filter(email=cd).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        else:
            return cd