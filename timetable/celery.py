import os

from celery import Celery
from celery.schedules import crontab

from timetable.settings import DAILY_UPDATE_HOUR

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timetable.settings')

app = Celery('timetable')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'process timetable daily update': {
        'task': 'daily_update',
        'schedule': crontab(hour=DAILY_UPDATE_HOUR, minute='0')
    },
}

