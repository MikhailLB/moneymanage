from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView

from reminders.models import Reminders


class NotificationsListView(LoginRequiredMixin, ListView):
    model = Reminders
    template_name = 'reminders/reminders.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        query_set = super().get_queryset()
        query_set = query_set.filter(user=self.request.user).order_by('-date')
        return query_set

@login_required
def delete_reminder(request, pk):
    reminder = get_object_or_404(Reminders, pk=pk, user=request.user)
    reminder.delete()
    return redirect('reminders')  # Замените 'reminders' на имя вашего маршрута