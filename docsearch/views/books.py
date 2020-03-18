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


class BookSearch(base_views.BaseSearchView):
    model = models.Book
    template_name = 'docsearch/books/search.html'
    facet_fields = ['township_arr', 'range_arr', 'section_arr']
    facet_field_name_overrides = {
        'section_arr': 'section',
        'township_arr': 'township',
        'range_arr': 'range'
    }
    sort_fields = facet_fields


class BookData(base_views.BaseDocumentData):
    document_model = models.Book
