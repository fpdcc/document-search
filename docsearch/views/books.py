from django.urls import reverse_lazy

from docsearch import models
from . import base as base_views


class BookDetail(base_views.BaseDetailView):
    model = models.Book
    template_name = 'docsearch/book/detail.html'
    update_url = 'book-update'


class BookCreate(base_views.BaseCreateView):
    model = models.Book
    template_name = 'docsearch/book/form.html'
    fields = '__all__'
    cancel_url = 'home'  # TODO: Change this to Search


class BookUpdate(base_views.BaseUpdateView):
    model = models.Book
    template_name = 'docsearch/book/form.html'
    fields = '__all__'
    cancel_url = 'book-detail'
    delete_url = 'book-delete'


class BookDelete(base_views.BaseDeleteView):
    model = models.Book
    template_name = 'docsearch/book/confirm_delete.html'
    cancel_url = 'book-detail'
    success_url = reverse_lazy('book-create')  # TODO: Change to search
