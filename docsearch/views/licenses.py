from docsearch import models
from . import base as base_views


class LicenseDetail(base_views.BaseDetailView):
    model = models.License
    template_name = 'docsearch/licenses/detail.html'
    metadata_fields = ['license_number', 'description', 'source_file']


class LicenseCreate(base_views.BaseCreateView):
    model = models.License
    template_name = 'docsearch/licenses/form.html'
    fields = '__all__'


class LicenseUpdate(base_views.BaseUpdateView):
    model = models.License
    template_name = 'docsearch/licenses/form.html'
    fields = '__all__'


class LicenseDelete(base_views.BaseDeleteView):
    model = models.License
    template_name = 'docsearch/licenses/confirm_delete.html'


class LicenseSearch(base_views.BaseSearchView):
    model = models.License
    template_name = 'docsearch/licenses/search.html'
    facet_fields = ['license_number']
    sort_fields = ['license_number', 'description_exact']
