from docsearch import models
from leaflet.forms.widgets import LeafletWidget
from django.contrib.gis.geos import GEOSException, GEOSGeometry
from django.contrib.gis.gdal.error import GDALException
import logging

from docsearch.forms import LicenseForm
from . import base as base_views

logger = logging.getLogger("django.contrib.gis")

class StricterLeafletWidget(LeafletWidget):
    def deserialize(self, value):
        try:
            return GEOSGeometry(value)
        except (GEOSException, ValueError, TypeError, GDALException) as err:
            logger.error("Error creating geometry from value '%s' (%s)", value, err)
        return None
    
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        if not context['serialized'] and isinstance(value, str):
            context['serialized'] = value
        return context

class MapWidgetMixin:
    def get_form(self):
        form = super().get_form()
        form.fields['geometry'].widget = StricterLeafletWidget(attrs={
            'map_height': '400px',
            'map_width': '100%',
            'display_raw': True
        })
        return form


class LicenseDetail(base_views.BaseDetailView):
    model = models.License
    template_name = 'docsearch/licenses/detail.html'
    metadata_fields = [
        'license_number', 'description', 'type', 'entity', 'diameter',
        'material', 'end_date', 'status', 'agreement_type', 'township',
        'range', 'section', 'source_file',
    ]
    array_fields = ['township', 'range', 'section']


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
    facet_fields = [
        'license_number', 'township_arr', 'range_arr', 'section_arr',
        'type', 'status', 'end_date', 'agreement_type'
    ]
    facet_field_name_overrides = {
        'section_arr': 'section',
        'township_arr': 'township',
        'range_arr': 'range'
    }
    sort_fields = [
        'license_number_exact', 'description_exact', 'township_arr', 'range_arr',
        'section_arr', 'type_exact', 'status_exact', 'end_date_exact',
        'agreement_type_exact'
    ]


class LicenseData(base_views.BaseDocumentData):
    document_model = models.License
