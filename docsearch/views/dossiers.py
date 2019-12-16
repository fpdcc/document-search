from docsearch import models
from . import base as base_views


class DossierDetail(base_views.BaseDetailView):
    model = models.Dossier
    template_name = 'docsearch/dossiers/detail.html'
    metadata_fields = ['file_number', 'document_number', 'source_file']


class DossierCreate(base_views.BaseCreateView):
    model = models.Dossier
    template_name = 'docsearch/dossiers/form.html'
    fields = '__all__'


class DossierUpdate(base_views.BaseUpdateView):
    model = models.Dossier
    template_name = 'docsearch/dossiers/form.html'
    fields = '__all__'


class DossierDelete(base_views.BaseDeleteView):
    model = models.Dossier
    template_name = 'docsearch/dossiers/confirm_delete.html'


class DossierSearch(base_views.BaseSearchView):
    model = models.Dossier
