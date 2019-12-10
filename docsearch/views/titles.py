from django.urls import reverse_lazy

from docsearch import models
from . import base as base_views


class TitleDetail(base_views.BaseDetailView):
    model = models.Title
    template_name = 'docsearch/titles/detail.html'
    update_url_from_obj = 'title-update'
    metadata_fields = ['control_number', 'source_file']


class TitleCreate(base_views.BaseCreateView):
    model = models.Title
    template_name = 'docsearch/titles/form.html'
    fields = '__all__'
    cancel_url = reverse_lazy('search', args=('titles',))


class TitleUpdate(base_views.BaseUpdateView):
    model = models.Title
    template_name = 'docsearch/titles/form.html'
    fields = '__all__'
    cancel_url_from_obj = 'title-detail'
    delete_url_from_obj = 'title-delete'


class TitleDelete(base_views.BaseDeleteView):
    model = models.Title
    template_name = 'docsearch/titles/confirm_delete.html'
    cancel_url_from_obj = 'title-detail'
    success_url = reverse_lazy('search', args=('titles',))
