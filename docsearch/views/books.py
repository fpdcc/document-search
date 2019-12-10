from django.urls import reverse_lazy

from docsearch import models
from . import base as base_views


class BookDetail(base_views.BaseDetailView):
    model = models.Book
    template_name = 'docsearch/books/detail.html'
    update_url_from_obj = 'book-update'
    metadata_fields = ['township', 'range', 'section', 'source_file']


class BookCreate(base_views.BaseCreateView):
    model = models.Book
    template_name = 'docsearch/books/form.html'
    fields = '__all__'
    cancel_url = reverse_lazy('search', args=('books',))


class BookUpdate(base_views.BaseUpdateView):
    model = models.Book
    template_name = 'docsearch/books/form.html'
    fields = '__all__'
    cancel_url_from_obj = 'book-detail'
    delete_url_from_obj = 'book-delete'


class BookDelete(base_views.BaseDeleteView):
    model = models.Book
    template_name = 'docsearch/books/confirm_delete.html'
    cancel_url_from_obj = 'book-detail'
    success_url = reverse_lazy('search', args=('books',))
