from django.urls import reverse_lazy

from docsearch import models
from . import base as base_views


class ControlMonumentMapDetail(base_views.BaseDetailView):
    model = models.ControlMonumentMap
    template_name = 'docsearch/controlmonumentmaps/detail.html'
    update_url_from_obj = 'controlmonumentmap-update'
    metadata_fields = ['township', 'range', 'section', 'part_of_section',
                       'source_file']


class ControlMonumentMapCreate(base_views.BaseCreateView):
    model = models.ControlMonumentMap
    template_name = 'docsearch/controlmonumentmaps/form.html'
    fields = '__all__'
    cancel_url = reverse_lazy('search', args=('controlmonumentmaps',))


class ControlMonumentMapUpdate(base_views.BaseUpdateView):
    model = models.ControlMonumentMap
    template_name = 'docsearch/controlmonumentmaps/form.html'
    fields = '__all__'
    cancel_url_from_obj = 'controlmonumentmap-detail'
    delete_url_from_obj = 'controlmonumentmap-delete'


class ControlMonumentMapDelete(base_views.BaseDeleteView):
    model = models.ControlMonumentMap
    template_name = 'docsearch/controlmonumentmaps/confirm_delete.html'
    cancel_url_from_obj = 'controlmonumentmap-detail'
    success_url = reverse_lazy('search', args=('controlmonumentmaps',))
