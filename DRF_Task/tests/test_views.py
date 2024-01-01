from api.models import Book
from api.views import BookViewSet
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate


class BookViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = BookViewSet.as_view(
            {
                "get": "retrieve",
                "post": "create",
                "put": "update",
                "patch": "partial_update",
            }
        )
        self.user = get_user_model().objects.create_user(
            email="zain@gmail.com",
            name="zain",
            password="admin",
            is_author=True,
        )
        self.book_data = {
            "id": "1",
            "title": "Test Book",
            "description": "xyz",
            "cover_img": "/media/images/att_Nctgurx.jpg",
            "author": "3",
            "in_stock": "True",
            "created": "2023-12-26",
        }
        self.b_data = {"title": "Test Book", "created": "2023-12-26"}
        self.book = Book.objects.create(
            title="Test Book", author=self.user, created="2023-12-26"
        )

    def test_retrieve_book(self):
        pk = self.book_data["id"]
        request = self.factory.get(f"/epicbooks/{pk}/")
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.book.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book(self):
        request = self.factory.post("api:epicbooks", self.b_data)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_book(self):
        pk = self.book_data["id"]
        request = self.factory.put(f"/epicbooks/{pk}/", self.book_data)

        force_authenticate(request, user=self.user)
        response = self.view(request, pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_book(self):
        pk = self.book_data["id"]
        request = self.factory.patch(f"/epicbooks/{pk}/", self.book_data)

        force_authenticate(request, user=self.user)
        response = self.view(request, pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
