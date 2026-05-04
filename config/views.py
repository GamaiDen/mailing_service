from django.shortcuts import render
from django.utils import timezone
from django.core.cache import cache
from mailings.models import Mailing
from clients.models import Client
from attempts.models import Attempt


def home(request):
    cache_key = 'home_page_stats'
    stats = cache.get(cache_key)

    if stats is None:
        total_mailings = Mailing.objects.count()
        now = timezone.now()
        active_mailings = Mailing.objects.filter(start_time__lte=now, end_time__gte=now).count()
        unique_clients = Client.objects.count()
        stats = {
            'total_mailings': total_mailings,
            'active_mailings': active_mailings,
            'unique_clients': unique_clients,
        }
        cache.set(cache_key, stats, timeout=60)

    if request.user.is_authenticated:
        my_mailings = Mailing.objects.filter(owner=request.user)
        successful = Attempt.objects.filter(mailing__in=my_mailings, status='Успешно').count()
        failed = Attempt.objects.filter(mailing__in=my_mailings, status='Не успешно').count()
    else:
        successful = 0
        failed = 0

    return render(request, 'index.html', {
        **stats,
        'successful': successful,
        'failed': failed,
    })
