from docsearch import models
from . import base as base_views


class EasementDetail(base_views.BaseDetailView):
    model = models.Easement
    template_name = 'docsearch/easements/detail.html'
    metadata_fields = ['easement_number', 'description', 'source_file']


class EasementCreate(base_views.BaseCreateView):
    model = models.Easement
    template_name = 'docsearch/easements/form.html'
    fields = '__all__'


class EasementUpdate(base_views.BaseUpdateView):
    model = models.Easement
    template_name = 'docsearch/easements/form.html'
    fields = '__all__'


class EasementDelete(base_views.BaseDeleteView):
    model = models.Easement
    template_name = 'docsearch/easements/confirm_delete.html'


class EasementSearch(base_views.BaseSearchView):
    model = models.Easement
    template_name = 'docsearch/easements/search.html'
    facet_fields = ['easement_number']
    sort_fields = ['easement_number', 'description_exact'] 
