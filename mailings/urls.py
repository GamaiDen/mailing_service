from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.MailingListView.as_view(), name='mailing_list'),
    path('<int:pk>/', views.MailingDetailView.as_view(), name='mailing_detail'),
    path('create/', login_required(views.MailingCreateView.as_view()), name='mailing_create'),
    path('<int:pk>/edit/', login_required(views.MailingUpdateView.as_view()), name='mailing_update'),
    path('<int:pk>/delete/', login_required(views.MailingDeleteView.as_view()), name='mailing_delete'),
    path('<int:pk>/send/', login_required(views.MailingSendView.as_view()), name='mailing_send'),
]
