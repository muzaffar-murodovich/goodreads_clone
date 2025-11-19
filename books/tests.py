from django.test import TestCase
from django.urls import reverse
from .models import Book

class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse("list"))

        self.assertContains(response, "No books found")

    def test_books_list(self):
        Book.objects.create(title="Book 1", description="Book 1 description", isbn="123456789")
        Book.objects.create(title="Book 2", description="Book 2 description", isbn="223456789")
        Book.objects.create(title="Book 3", description="Book 3 description", isbn="323456789")

        response = self.client.get(reverse("list"))

        books = Book.objects.all()
        for book in books:
            self.assertContains(response, book.title)

    def test_detail_page(self):
        book = Book.objects.create(title="Book 1", description="Book 1 description", isbn="123456789")
        response = self.client.get(reverse("detail", kwargs={"id": book.id }))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)
