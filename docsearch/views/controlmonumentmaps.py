from django.urls import reverse_lazy

from docsearch import models
from . import base as base_views


class ControlMonumentMapDetail(base_views.BaseDetailView):
    model = models.ControlMonumentMap
    template_name = 'docsearch/controlmonumentmap/detail.html'
    update_url = 'controlmonumentmap-update'


class ControlMonumentMapCreate(base_views.BaseCreateView):
    model = models.ControlMonumentMap
    template_name = 'docsearch/controlmonumentmap/form.html'
    fields = '__all__'
    cancel_url = 'home'  # TODO: Change this to Search


class ControlMonumentMapUpdate(base_views.BaseUpdateView):
    model = models.ControlMonumentMap
    template_name = 'docsearch/controlmonumentmap/form.html'
    fields = '__all__'
    cancel_url = 'controlmonumentmap-detail'
    delete_url = 'controlmonumentmap-delete'


class ControlMonumentMapDelete(base_views.BaseDeleteView):
    model = models.ControlMonumentMap
    template_name = 'docsearch/controlmonumentmap/confirm_delete.html'
    cancel_url = 'controlmonumentmap-detail'
    success_url = reverse_lazy('controlmonumentmap-create')  # TODO: Change to search
