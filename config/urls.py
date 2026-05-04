from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('clients/', include('clients.urls')),
    path('messages/', include('messages_app.urls')),
    path('mailings/', include('mailings.urls')),
    path('users/', include('users.urls')),
]
