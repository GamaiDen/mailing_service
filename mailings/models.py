from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('Создана', 'Создана'),
        ('Запущена', 'Запущена'),
        ('Завершена', 'Завершена'),
    ]

    start_time = models.DateTimeField(verbose_name='Дата и время начала отправки')
    end_time = models.DateTimeField(verbose_name='Дата и время окончания отправки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Создана', verbose_name='Статус')
    message = models.ForeignKey('messages_app.Message', on_delete=models.CASCADE, verbose_name='Сообщение')
    recipients = models.ManyToManyField('clients.Client', verbose_name='Получатели')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return f"Рассылка {self.pk} ({self.status})"

    def clean(self):
        if self.start_time and self.start_time < timezone.now():
            raise ValidationError('Дата начала не может быть в прошлом.')
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError('Дата начала должна быть раньше даты окончания.')

    def update_status(self):
        now = timezone.now()
        if now < self.start_time:
            new_status = 'Создана'
        elif self.start_time <= now <= self.end_time:
            new_status = 'Запущена'
        else:
            new_status = 'Завершена'
        if self.status != new_status:
            self.status = new_status
            self.save(update_fields=['status'])
