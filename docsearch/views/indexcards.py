from django.urls import reverse_lazy

from docsearch import models
from . import base as base_views


class IndexCardDetail(base_views.BaseDetailView):
    model = models.IndexCard
    template_name = 'docsearch/indexcards/detail.html'
    update_url_from_obj = 'indexcard-update'
    metadata_fields = ['monument_number', 'township', 'section', 'corner',
                       'source_file']


class IndexCardCreate(base_views.BaseCreateView):
    model = models.IndexCard
    template_name = 'docsearch/indexcards/form.html'
    fields = '__all__'
    cancel_url = reverse_lazy('search', args=('indexcards',))


class IndexCardUpdate(base_views.BaseUpdateView):
    model = models.IndexCard
    template_name = 'docsearch/indexcards/form.html'
    fields = '__all__'
    cancel_url_from_obj = 'indexcard-detail'
    delete_url_from_obj = 'indexcard-delete'


class IndexCardDelete(base_views.BaseDeleteView):
    model = models.IndexCard
    template_name = 'docsearch/indexcards/confirm_delete.html'
    cancel_url_from_obj = 'indexcard-detail'
    success_url = reverse_lazy('search', args=('indexcards',))
