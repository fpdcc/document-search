from docsearch import models
from . import base as base_views


class IndexCardDetail(base_views.BaseDetailView):
    model = models.IndexCard
    template_name = 'docsearch/indexcards/detail.html'
    metadata_fields = ['monument_number', 'township', 'section', 'corner',
                       'source_file']


class IndexCardCreate(base_views.BaseCreateView):
    model = models.IndexCard
    template_name = 'docsearch/indexcards/form.html'
    fields = '__all__'


class IndexCardUpdate(base_views.BaseUpdateView):
    model = models.IndexCard
    template_name = 'docsearch/indexcards/form.html'
    fields = '__all__'


class IndexCardDelete(base_views.BaseDeleteView):
    model = models.IndexCard
    template_name = 'docsearch/indexcards/confirm_delete.html'


class IndexCardSearch(base_views.BaseSearchView):
    model = models.IndexCard
    template_name = 'docsearch/indexcards/search.html'
    facet_fields = ['monument_number', 'township', 'section', 'corner']
    sort_fields = ['monument_number_exact', 'township', 'section_exact', 'corner_exact']


class IndexCardData(base_views.BaseDocumentData):
    document_model = models.IndexCard
