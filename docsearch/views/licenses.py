from django.urls import reverse_lazy

from docsearch import models
from . import base as base_views


class LicenseDetail(base_views.BaseDetailView):
    model = models.License
    template_name = 'docsearch/licenses/detail.html'
    update_url_from_obj = 'license-update'
    metadata_fields = ['license_number', 'source_file']


class LicenseCreate(base_views.BaseCreateView):
    model = models.License
    template_name = 'docsearch/licenses/form.html'
    fields = '__all__'
    cancel_url = reverse_lazy('search', args=('licenses',))


class LicenseUpdate(base_views.BaseUpdateView):
    model = models.License
    template_name = 'docsearch/licenses/form.html'
    fields = '__all__'
    cancel_url_from_obj = 'license-detail'
    delete_url_from_obj = 'license-delete'


class LicenseDelete(base_views.BaseDeleteView):
    model = models.License
    template_name = 'docsearch/licenses/confirm_delete.html'
    cancel_url_from_obj = 'license-detail'
    success_url = reverse_lazy('search', args=('licenses',))
