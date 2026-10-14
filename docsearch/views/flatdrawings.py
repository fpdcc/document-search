from django.db import transaction

from docsearch import models, forms
from . import base as base_views


class FlatDrawingDetail(base_views.BaseDetailView):
    model = models.FlatDrawing
    template_name = 'docsearch/flatdrawings/detail.html'
    metadata_fields = ['coordinates', 'area', 'section', 'map_number', 'location', 'building_id',
                       'description', 'job_number', 'number_of_sheets',
                       'date', 'cross_ref_area', 'cross_ref_section',
                       'cross_ref_map_number', 'hash', 'cad_file',
                       'source_file']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        # Supply the coordinates for this FlatDrawing
        context['coordinates'] = (
            context['object'].coordinates.all()
            .order_by("id")
            .values_list("area", "section", named=True)
        )
        return context


class CoordinateFormSetMixin:
    """Edit a FlatDrawing's Coordinates alongside the FlatDrawing itself."""

    def get_coordinate_formset(self):
        kwargs = {'instance': self.object, 'prefix': 'coordinates'}
        if self.request.method == 'POST':
            kwargs.update(data=self.request.POST, files=self.request.FILES)
        return forms.CoordinateFormSet(**kwargs)

    def get_context_data(self, **kwargs):
        # On GET, build an unbound formset
        # On an invalid POST, return a sticky/bound form with errors
        if 'coordinate_formset' not in kwargs:
            kwargs['coordinate_formset'] = self.get_coordinate_formset()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        formset = self.get_coordinate_formset()
        if not formset.is_valid():
            return self.form_invalid(form, formset)

        with transaction.atomic():
            # Save the FlatDrawing and build the redirect
            response = super().form_valid(form)
            # On create, the formset was built before the FlatDrawing had a pk
            formset.instance = self.object
            formset.save()
        return response

    def form_invalid(self, form, formset=None):
        if formset is None:
            formset = self.get_coordinate_formset()
        return self.render_to_response(
            self.get_context_data(form=form, coordinate_formset=formset)
        )


class FlatDrawingCreate(CoordinateFormSetMixin, base_views.BaseCreateView):
    model = models.FlatDrawing
    template_name = 'docsearch/flatdrawings/form.html'
    fields = '__all__'


class FlatDrawingUpdate(CoordinateFormSetMixin, base_views.BaseUpdateView):
    model = models.FlatDrawing
    template_name = 'docsearch/flatdrawings/form.html'
    fields = '__all__'


class FlatDrawingDelete(base_views.BaseDeleteView):
    model = models.FlatDrawing
    template_name = 'docsearch/flatdrawings/confirm_delete.html'


class FlatDrawingSearch(base_views.BaseSearchView):
    # TODO: add Coordinate obj area and section to the facet fields, and make them functional
    model = models.FlatDrawing
    template_name = 'docsearch/flatdrawings/search.html'
    facet_fields = ['area', 'section', 'map_number', 'location', 'building_id',
                    'job_number', 'number_of_sheets', 'date', 'cross_ref_area',
                    'cross_ref_section', 'cross_ref_map_number']
    sort_fields = ['area', 'section_exact', 'map_number_exact', 'location_exact',
                   'building_id', 'description_exact', 'job_number_exact',
                   'number_of_sheets_exact', 'date_exact', 'cross_ref_area',
                   'cross_ref_section', 'cross_ref_map_number_exact']


class FlatDrawingData(base_views.BaseDocumentData):
    document_model = models.FlatDrawing
