from celery import Celery, shared_task
from .models import Book

app = Celery("tasks", broker="pyamqp://guest@localhost//")

# @app.task
# def add(x, y):
#     return x + y


@shared_task
def apply_discount():
    books = Book.objects.all()
    for book in books:
        book.price *= 0.9  # Apply a 10% discount
        book.save()
