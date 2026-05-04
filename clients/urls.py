from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.ClientListView.as_view(), name='client_list'),
    path('create/', login_required(views.ClientCreateView.as_view()), name='client_create'),
    path('<int:pk>/edit/', login_required(views.ClientUpdateView.as_view()), name='client_update'),
    path('<int:pk>/delete/', login_required(views.ClientDeleteView.as_view()), name='client_delete'),
]
