from docsearch import models
from . import base as base_views


class SurplusParcelDetail(base_views.BaseDetailView):
    model = models.SurplusParcel
    template_name = 'docsearch/surplusparcels/detail.html'
    metadata_fields = ['surplus_parcel', 'description', 'source_file']


class SurplusParcelCreate(base_views.BaseCreateView):
    model = models.SurplusParcel
    template_name = 'docsearch/surplusparcels/form.html'
    fields = '__all__'


class SurplusParcelUpdate(base_views.BaseUpdateView):
    model = models.SurplusParcel
    template_name = 'docsearch/surplusparcels/form.html'
    fields = '__all__'


class SurplusParcelDelete(base_views.BaseDeleteView):
    model = models.SurplusParcel
    template_name = 'docsearch/surplusparcels/confirm_delete.html'


class SurplusParcelSearch(base_views.BaseSearchView):
    model = models.SurplusParcel
    template_name = 'docsearch/surplusparcels/search.html'
    facet_fields = ['surplus_parcel']
    search_fields = facet_fields
    sort_fields = facet_fields + ['description_exact']
