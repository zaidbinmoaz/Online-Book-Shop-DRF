import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EpicBooks.settings")

app = Celery("EpicBooks")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")


# celery beat settings
app.conf.beat_schedule = {
    " discount_on_books": {
        "task": "api.tasks.apply_discount",
        "schedule": crontab(minute="*/1"),
    },
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
