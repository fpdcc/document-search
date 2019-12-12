from docsearch import models
from . import base as base_views


class BookDetail(base_views.BaseDetailView):
    model = models.Book
    template_name = 'docsearch/books/detail.html'
    metadata_fields = ['township', 'range', 'section', 'source_file']


class BookCreate(base_views.BaseCreateView):
    model = models.Book
    template_name = 'docsearch/books/form.html'
    fields = '__all__'


class BookUpdate(base_views.BaseUpdateView):
    model = models.Book
    template_name = 'docsearch/books/form.html'
    fields = '__all__'


class BookDelete(base_views.BaseDeleteView):
    model = models.Book
    template_name = 'docsearch/books/confirm_delete.html'
