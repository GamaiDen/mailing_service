from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Message
from .forms import MessageForm


class MessageListView(ListView):
    model = Message
    template_name = 'messages_app/message_list.html'
    context_object_name = 'messages'


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'messages_app/message_form.html'
    success_url = reverse_lazy('message_list')


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'messages_app/message_form.html'
    success_url = reverse_lazy('message_list')


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'messages_app/message_confirm_delete.html'
    success_url = reverse_lazy('message_list')
