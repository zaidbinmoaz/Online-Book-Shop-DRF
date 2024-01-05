import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EpicBooks.settings")

app = Celery("EpicBooks")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


# @Celery.periodic_task(run_every=timedelta(minutes=1))
# def apply_discount():
#     books = Book.objects.all()
#     for book in books:
#         book.price *= 0.9  # Apply a 10% discount
#         book.save()
