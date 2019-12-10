from django.urls import reverse_lazy

from docsearch import models
from . import base as base_views


class RightOfWayDetail(base_views.BaseDetailView):
    model = models.RightOfWay
    template_name = 'docsearch/rightsofway/detail.html'
    update_url_from_obj = 'rightofway-update'
    metadata_fields = ['folder_tab', 'source_file']


class RightOfWayCreate(base_views.BaseCreateView):
    model = models.RightOfWay
    template_name = 'docsearch/rightsofway/form.html'
    fields = '__all__'
    cancel_url = reverse_lazy('search', args=('rightsofway',))


class RightOfWayUpdate(base_views.BaseUpdateView):
    model = models.RightOfWay
    template_name = 'docsearch/rightsofway/form.html'
    fields = '__all__'
    cancel_url_from_obj = 'rightofway-detail'
    delete_url_from_obj = 'rightofway-delete'


class RightOfWayDelete(base_views.BaseDeleteView):
    model = models.RightOfWay
    template_name = 'docsearch/rightsofway/confirm_delete.html'
    cancel_url_from_obj = 'rightofway-detail'
    success_url = reverse_lazy('search', args=('rightsofway',))
