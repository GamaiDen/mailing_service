from django.contrib import admin
from .models import Mailing

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'start_time', 'end_time')
