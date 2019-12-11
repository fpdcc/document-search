from docsearch import models
from . import base as base_views


class TitleDetail(base_views.BaseDetailView):
    model = models.Title
    template_name = 'docsearch/titles/detail.html'
    metadata_fields = ['control_number', 'source_file']


class TitleCreate(base_views.BaseCreateView):
    model = models.Title
    template_name = 'docsearch/titles/form.html'
    fields = '__all__'


class TitleUpdate(base_views.BaseUpdateView):
    model = models.Title
    template_name = 'docsearch/titles/form.html'
    fields = '__all__'


class TitleDelete(base_views.BaseDeleteView):
    model = models.Title
    template_name = 'docsearch/titles/confirm_delete.html'
