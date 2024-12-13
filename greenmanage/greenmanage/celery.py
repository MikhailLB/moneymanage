from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greenmanage.settings')

app = Celery('greenmanage')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-rates-every-hour': {
        'task': 'currencies.tasks.get_beat_currencies',
        'schedule': crontab(minute=0, hour='*/1')
    },
    'check_auto_payments': {
        'task': 'temp_transactions.tasks.process_auto_payments',
        'schedule': crontab(minute='*/1')
    },
}

