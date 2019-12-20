from docsearch import models
from . import base as base_views


class DeepTunnelDetail(base_views.BaseDetailView):
    model = models.DeepTunnel
    template_name = 'docsearch/deeptunnels/detail.html'
    metadata_fields = ['description', 'source_file']


class DeepTunnelCreate(base_views.BaseCreateView):
    model = models.DeepTunnel
    template_name = 'docsearch/deeptunnels/form.html'
    fields = '__all__'


class DeepTunnelUpdate(base_views.BaseUpdateView):
    model = models.DeepTunnel
    template_name = 'docsearch/deeptunnels/form.html'
    fields = '__all__'


class DeepTunnelDelete(base_views.BaseDeleteView):
    model = models.DeepTunnel
    template_name = 'docsearch/deeptunnels/confirm_delete.html'


class DeepTunnelSearch(base_views.BaseSearchView):
    model = models.DeepTunnel
    template_name = 'docsearch/deeptunnels/search.html'
    facet_fields = []
