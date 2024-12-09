from locale import currency

from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.models import Account
from reminders.tasks import change_password_notification, forgot_password_notification
from .forms import LoginUserForm, RegisterUserForm, UserPasswordChangeForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        if not Account.objects.filter(user=self.request.user).exists():
            account = Account.objects.create(user=self.request.user, name=self.request.user.first_name)
            account.save()
        return reverse_lazy('dashboard')



def logout_user(request):

    logout(request)
    return redirect('users:login')

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/password_reset.html'

    def get_success_url(self):
        forgot_password_notification(self.request.user)
        return reverse_lazy('users:password-change-done')

class PasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'users/password_change.html'

    def get_success_url(self):
        change_password_notification(self.request.user)
        return reverse_lazy('users:password-change-done')
# def register(request):
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password1'])
#             form.save()
#             return render(request, "users/login.html")
#     else:
#         form = RegisterUserForm()
#     return render(request, "users/register.html", {"form":form})