from django.db import models
from django.conf import settings


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=200, verbose_name='Ф.И.О.')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец')

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'

    def __str__(self):
        return f"{self.full_name} ({self.email})"
