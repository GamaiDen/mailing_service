from django.db import models


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('Создана', 'Создана'),
        ('Запущена', 'Запущена'),
        ('Завершена', 'Завершена'),
    ]

    first_send_at = models.DateTimeField(verbose_name='Дата и время первой отправки')
    end_send_at = models.DateTimeField(verbose_name='Дата и время окончания отправки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Создана', verbose_name='Статус')
    message = models.ForeignKey('messages_app.Message', on_delete=models.CASCADE, verbose_name='Сообщение')
    clients = models.ManyToManyField('clients.Client', verbose_name='Получатели')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return f"Рассылка {self.pk} ({self.status})"
