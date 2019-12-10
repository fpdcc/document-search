from django.urls import reverse_lazy

from docsearch import models
from . import base as base_views


class EasementDetail(base_views.BaseDetailView):
    model = models.Easement
    template_name = 'docsearch/easements/detail.html'
    update_url_from_obj = 'easement-update'
    metadata_fields = ['easement_number', 'source_file']


class EasementCreate(base_views.BaseCreateView):
    model = models.Easement
    template_name = 'docsearch/easements/form.html'
    fields = '__all__'
    cancel_url = reverse_lazy('search', args=('easements',))


class EasementUpdate(base_views.BaseUpdateView):
    model = models.Easement
    template_name = 'docsearch/easements/form.html'
    fields = '__all__'
    cancel_url_from_obj = 'easement-detail'
    delete_url_from_obj = 'easement-delete'


class EasementDelete(base_views.BaseDeleteView):
    model = models.Easement
    template_name = 'docsearch/easements/confirm_delete.html'
    cancel_url_from_obj = 'easement-detail'
    success_url = reverse_lazy('search', args=('easements',))
