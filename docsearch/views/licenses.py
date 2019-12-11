from docsearch import models
from . import base as base_views


class LicenseDetail(base_views.BaseDetailView):
    model = models.License
    template_name = 'docsearch/licenses/detail.html'
    metadata_fields = ['license_number', 'source_file']


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
