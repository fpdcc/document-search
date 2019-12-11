from docsearch import models
from . import base as base_views


class RightOfWayDetail(base_views.BaseDetailView):
    model = models.RightOfWay
    template_name = 'docsearch/rightsofway/detail.html'
    metadata_fields = ['folder_tab', 'source_file']


class RightOfWayCreate(base_views.BaseCreateView):
    model = models.RightOfWay
    template_name = 'docsearch/rightsofway/form.html'
    fields = '__all__'


class RightOfWayUpdate(base_views.BaseUpdateView):
    model = models.RightOfWay
    template_name = 'docsearch/rightsofway/form.html'
    fields = '__all__'


class RightOfWayDelete(base_views.BaseDeleteView):
    model = models.RightOfWay
    template_name = 'docsearch/rightsofway/confirm_delete.html'
