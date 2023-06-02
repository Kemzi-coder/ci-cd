from django.test import TestCase
from django.urls import reverse
from .models import Book, Author

# Create your tests here.

class BookListViewTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='John Doe', bio='Author bio')
        self.book1 = Book.objects.create(title='Book 1', publication_date='2023-01-01', price=10.99)
        self.book2 = Book.objects.create(title='Book 2', publication_date='2023-02-01', price=12.99)
        self.book1.authors.add(self.author)
        self.book2.authors.add(self.author)
        self.url = reverse('book_list')

    def test_book_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_list.html')
        self.assertContains(response, self.book1.title)
        self.assertContains(response, self.book2.title)

    def test_book_list_view_no_books(self):
        Book.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_list.html')
        self.assertContains(response, 'No books available.')


class BookDetailViewTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='John Doe', bio='Author bio')
        self.book = Book.objects.create(title='Book 1', publication_date='2023-01-01', price=10.99)
        self.book.authors.add(self.author)
        self.url = reverse('book_detail', args=[self.book.id])

    def test_book_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_detail.html')
        self.assertContains(response, self.book.title)
        self.assertContains(response, self.author.name)
        self.assertContains(response, self.book.price)

    def test_book_detail_view_invalid_id(self):
        invalid_id = self.book.id + 1  # Assuming the next ID is invalid
        url = reverse('book_detail', args=[invalid_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
