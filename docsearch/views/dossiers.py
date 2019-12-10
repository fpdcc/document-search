from django.urls import reverse_lazy

from docsearch import models
from . import base as base_views


class DossierDetail(base_views.BaseDetailView):
    model = models.Dossier
    template_name = 'docsearch/dossiers/detail.html'
    update_url_from_obj = 'dossier-update'
    metadata_fields = ['file_number', 'document_number', 'source_file']


class DossierCreate(base_views.BaseCreateView):
    model = models.Dossier
    template_name = 'docsearch/dossiers/form.html'
    fields = '__all__'
    cancel_url = reverse_lazy('search', args=('dossiers',))


class DossierUpdate(base_views.BaseUpdateView):
    model = models.Dossier
    template_name = 'docsearch/dossiers/form.html'
    fields = '__all__'
    cancel_url_from_obj = 'dossier-detail'
    delete_url_from_obj = 'dossier-delete'


class DossierDelete(base_views.BaseDeleteView):
    model = models.Dossier
    template_name = 'docsearch/dossiers/confirm_delete.html'
    cancel_url_from_obj = 'dossier-detail'
    success_url = reverse_lazy('search', args=('dossiers',))
