from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Attempt


class AttemptListView(LoginRequiredMixin, ListView):
    model = Attempt
    template_name = 'attempts/attempt_list.html'
    context_object_name = 'attempts'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Attempt.objects.all()
        return Attempt.objects.filter(mailing__owner=user)
