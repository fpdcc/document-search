from django.urls import reverse_lazy

from docsearch import models
from . import base as base_views


class FlatDrawingDetail(base_views.BaseDetailView):
    model = models.FlatDrawing
    template_name = 'docsearch/flatdrawings/detail.html'
    update_url_from_obj = 'flatdrawing-update'
    metadata_fields = ['area', 'section', 'map_number', 'location',
                       'description', 'job_number', 'number_of_sheets',
                       'date', 'cross_ref_area', 'cross_ref_section',
                       'cross_ref_map_number', 'hash', 'cad_file',
                       'source_file']


class FlatDrawingCreate(base_views.BaseCreateView):
    model = models.FlatDrawing
    template_name = 'docsearch/flatdrawings/form.html'
    fields = '__all__'
    cancel_url = reverse_lazy('search', args=('flatdrawings',))


class FlatDrawingUpdate(base_views.BaseUpdateView):
    model = models.FlatDrawing
    template_name = 'docsearch/flatdrawings/form.html'
    fields = '__all__'
    cancel_url_from_obj = 'flatdrawing-detail'
    delete_url_from_obj = 'flatdrawing-delete'


class FlatDrawingDelete(base_views.BaseDeleteView):
    model = models.FlatDrawing
    template_name = 'docsearch/flatdrawings/confirm_delete.html'
    cancel_url_from_obj = 'flatdrawing-detail'
    success_url = reverse_lazy('search', args=('flatdrawings',))
