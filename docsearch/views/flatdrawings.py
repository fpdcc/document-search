from docsearch import models
from . import base as base_views


class FlatDrawingDetail(base_views.BaseDetailView):
    model = models.FlatDrawing
    template_name = 'docsearch/flatdrawings/detail.html'
    metadata_fields = ['area', 'section', 'map_number', 'location',
                       'description', 'job_number', 'number_of_sheets',
                       'date', 'cross_ref_area', 'cross_ref_section',
                       'cross_ref_map_number', 'hash', 'cad_file',
                       'source_file']


class FlatDrawingCreate(base_views.BaseCreateView):
    model = models.FlatDrawing
    template_name = 'docsearch/flatdrawings/form.html'
    fields = '__all__'


class FlatDrawingUpdate(base_views.BaseUpdateView):
    model = models.FlatDrawing
    template_name = 'docsearch/flatdrawings/form.html'
    fields = '__all__'


class FlatDrawingDelete(base_views.BaseDeleteView):
    model = models.FlatDrawing
    template_name = 'docsearch/flatdrawings/confirm_delete.html'


class FlatDrawingSearch(base_views.BaseSearchView):
    model = models.FlatDrawing
    template_name = 'docsearch/flatdrawings/search.html'
    facet_fields = ['section', 'map_number', 'location', 'job_number',
                    'number_of_sheets', 'date', 'cross_ref_area',
                    'cross_ref_section', 'cross_ref_map_number', 'hash']
