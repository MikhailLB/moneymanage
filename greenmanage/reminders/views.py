from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView

from reminders.models import Reminders


@login_required
def main(request):
    return render(request, 'reminders/reminders.html')


class NotificationsListView(ListView):
    model = Reminders
    template_name = 'reminders/reminders.html'
    context_object_name = 'reminders'

    def get_queryset(self):
        query_set = super().get_queryset()
        query_set = query_set.filter(user=self.request.user)
        return query_set