from docsearch import models
from . import base as base_views


class ControlMonumentMapDetail(base_views.BaseDetailView):
    model = models.ControlMonumentMap
    template_name = 'docsearch/controlmonumentmaps/detail.html'
    metadata_fields = ['township', 'range', 'section', 'part_of_section',
                       'source_file']


class ControlMonumentMapCreate(base_views.BaseCreateView):
    model = models.ControlMonumentMap
    template_name = 'docsearch/controlmonumentmaps/form.html'
    fields = '__all__'


class ControlMonumentMapUpdate(base_views.BaseUpdateView):
    model = models.ControlMonumentMap
    template_name = 'docsearch/controlmonumentmaps/form.html'
    fields = '__all__'


class ControlMonumentMapDelete(base_views.BaseDeleteView):
    model = models.ControlMonumentMap
    template_name = 'docsearch/controlmonumentmaps/confirm_delete.html'


class ControlMonumentMapSearch(base_views.BaseSearchView):
    model = models.ControlMonumentMap
    template_name = 'docsearch/controlmonumentmaps/search.html'
    facet_fields = ['section_arr', 'township', 'range', 'part_of_section']
    facet_field_name_overrides = {'section_arr': 'section'}
    sort_fields = ['section_arr', 'township', 'range', 'part_of_section_exact']
