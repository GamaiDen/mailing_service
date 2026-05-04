from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.core.mail import send_mail
from django.utils import timezone
from .models import Mailing
from .forms import MailingForm
from attempts.models import Attempt


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailings/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'
    context_object_name = 'mailing'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailing_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailing_list')


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_list')


class MailingSendView(LoginRequiredMixin, View):
    def post(self, request, pk):
        mailing = Mailing.objects.get(pk=pk)
        mailing.update_status()
        now = timezone.now()
        if now < mailing.start_time or now > mailing.end_time:
            messages.error(request, 'Сейчас не время для отправки этой рассылки.')
            return redirect('mailing_detail', pk=pk)
        clients = mailing.recipients.all()
        for client in clients:
            try:
                send_mail(mailing.message.subject, mailing.message.body, 'admin@mailing.ru', [client.email], fail_silently=False)
                Attempt.objects.create(mailing=mailing, status='Успешно', server_response='OK')
            except Exception as e:
                Attempt.objects.create(mailing=mailing, status='Не успешно', server_response=str(e))
        messages.success(request, 'Рассылка отправлена!')
        return redirect('mailing_detail', pk=pk)
