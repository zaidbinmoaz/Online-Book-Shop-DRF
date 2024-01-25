from celery import Celery, shared_task
from .models import Book

app = Celery("tasks", broker="pyamqp://guest@localhost//")


@shared_task
def apply_discount():
    books = Book.objects.all()
    for book in books:
        if book.price < 100:
            book.price = 500
        else:
            book.price *= 0.9  # Apply a 10% discount
        book.save()
