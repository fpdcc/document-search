from django.urls import reverse_lazy

from docsearch import models
from . import base as base_views


class SurplusParcelDetail(base_views.BaseDetailView):
    model = models.SurplusParcel
    template_name = 'docsearch/surplusparcels/detail.html'
    update_url_from_obj = 'surplusparcel-update'
    metadata_fields = ['surplus_parcel', 'description', 'source_file']


class SurplusParcelCreate(base_views.BaseCreateView):
    model = models.SurplusParcel
    template_name = 'docsearch/surplusparcels/form.html'
    fields = '__all__'
    cancel_url = reverse_lazy('search', args=('surplusparcels',))


class SurplusParcelUpdate(base_views.BaseUpdateView):
    model = models.SurplusParcel
    template_name = 'docsearch/surplusparcels/form.html'
    fields = '__all__'
    cancel_url_from_obj = 'surplusparcel-detail'
    delete_url_from_obj = 'surplusparcel-delete'


class SurplusParcelDelete(base_views.BaseDeleteView):
    model = models.SurplusParcel
    template_name = 'docsearch/surplusparcels/confirm_delete.html'
    cancel_url_from_obj = 'surplusparcel-detail'
    success_url = reverse_lazy('search', args=('surplusparcels',))
