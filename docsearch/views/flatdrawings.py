from django.db import transaction

from docsearch import models, forms
from . import base as base_views


class FlatDrawingDetail(base_views.BaseDetailView):
    model = models.FlatDrawing
    template_name = 'docsearch/flatdrawings/detail.html'
    metadata_fields = ['location_sets', 'map_number', 'location_name', 'building_id',
                       'description', 'job_number', 'number_of_sheets',
                       'date', 'cross_ref_map_number', 'hash', 'cad_file',
                       'source_file']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        # Supply the location sets for this FlatDrawing
        context['location_sets'] = (
            context['object'].location_sets.all()
            .order_by("id")
            .values_list("area", "section", named=True)
        )
        return context


class LocationSetFormSetMixin:
    """Edit a FlatDrawing's LocationSets alongside the FlatDrawing itself."""

    def get_location_set_formset(self):
        kwargs = {'instance': self.object, 'prefix': 'location_sets'}
        if self.request.method == 'POST':
            kwargs.update(data=self.request.POST, files=self.request.FILES)
        return forms.LocationSetFormSet(**kwargs)

    def get_context_data(self, **kwargs):
        # On GET, build an unbound formset
        # On an invalid POST, return a sticky/bound form with errors
        if 'location_set_formset' not in kwargs:
            kwargs['location_set_formset'] = self.get_location_set_formset()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        formset = self.get_location_set_formset()
        if not formset.is_valid():
            return self.form_invalid(form, formset)

        with transaction.atomic():
            # Save the LocationSets and build the redirect
            response = super().form_valid(form)
            # On create, the formset was built before the FlatDrawing had a pk
            formset.instance = self.object
            formset.save()

            # Save the FlatDrawing to reindex new LocationSet values
            formset.instance.save()
        return response

    def form_invalid(self, form, formset=None):
        if formset is None:
            formset = self.get_location_set_formset()
        return self.render_to_response(
            self.get_context_data(form=form, location_set_formset=formset)
        )


class FlatDrawingCreate(LocationSetFormSetMixin, base_views.BaseCreateView):
    model = models.FlatDrawing
    template_name = 'docsearch/flatdrawings/form.html'
    form_class = forms.FlatDrawingForm


class FlatDrawingUpdate(LocationSetFormSetMixin, base_views.BaseUpdateView):
    model = models.FlatDrawing
    template_name = 'docsearch/flatdrawings/form.html'
    form_class = forms.FlatDrawingForm


class FlatDrawingDelete(base_views.BaseDeleteView):
    model = models.FlatDrawing
    template_name = 'docsearch/flatdrawings/confirm_delete.html'


class FlatDrawingSearch(base_views.BaseSearchView):
    model = models.FlatDrawing
    template_name = 'docsearch/flatdrawings/search.html'
    facet_fields = ['location_set_areas', 'location_set_sections', 'map_number', 'location_name', 'building_id',
                    'job_number', 'number_of_sheets', 'date', 'cross_ref_map_number']
    sort_fields = ['location_set_areas', 'location_set_sections', 'map_number_exact', 'location_name_exact',
                   'building_id', 'description_exact', 'job_number_exact',
                   'number_of_sheets_exact', 'date_exact', 'cross_ref_map_number_exact']


class FlatDrawingData(base_views.BaseDocumentData):
    document_model = models.FlatDrawing
