from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from accounts.forms import UpdateProfileForm
from accounts.models import Account
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden

def main(request):
    return render(request, 'accounts/accounts.html')


class UpdateAccountView(LoginRequiredMixin, UpdateView):
    form_class = UpdateProfileForm
    template_name = 'accounts/update_accounts.html'
    success_url = reverse_lazy('accounts')

    def get_object(self, queryset=None):
        obj = get_object_or_404(get_user_model(), id=self.kwargs['pk'])
        if obj != self.request.user:
            return HttpResponseForbidden("You are not allowed to edit this profile.")

        return obj

    def form_valid(self, form):
        self.object = form.save()  # Сохраняет изменения в объекте профиля
        return super().form_valid(form)


