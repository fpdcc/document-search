from docsearch import models
from leaflet.forms.widgets import LeafletWidget

from docsearch.forms import LicenseForm
from . import base as base_views


class MapWidgetMixin:
    def get_form(self):
        form = super().get_form()
        form.fields['geometry'].widget = LeafletWidget(attrs={
            'map_height': '400px',
            'map_width': '100%',
            'display_raw': True
        })
        return form


class LicenseDetail(base_views.BaseDetailView):
    model = models.License
    template_name = 'docsearch/licenses/detail.html'
    metadata_fields = ['license_number', 'description', 'source_file']


class LicenseCreate(MapWidgetMixin, base_views.BaseCreateView):
    model = models.License
    template_name = 'docsearch/licenses/form.html'
    form_class = LicenseForm


class LicenseUpdate(MapWidgetMixin, base_views.BaseUpdateView):
    model = models.License
    template_name = 'docsearch/licenses/form.html'
    form_class = LicenseForm


class LicenseDelete(base_views.BaseDeleteView):
    model = models.License
    template_name = 'docsearch/licenses/confirm_delete.html'


class LicenseSearch(base_views.BaseSearchView):
    model = models.License
    template_name = 'docsearch/licenses/search.html'
    facet_fields = ['license_number']
    sort_fields = ['license_number', 'description_exact']
