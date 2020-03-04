from docsearch import models
from . import base as base_views


class SurveyDetail(base_views.BaseDetailView):
    model = models.Survey
    template_name = 'docsearch/surveys/detail.html'
    metadata_fields = ['township', 'range', 'section', 'map_number', 'location',
                       'description', 'job_number', 'number_of_sheets',
                       'date', 'cross_ref_area', 'cross_ref_section',
                       'cross_ref_map_number', 'hash', 'source_file']
    array_fields = ['township', 'range', 'section']


class SurveyCreate(base_views.BaseCreateView):
    model = models.Survey
    template_name = 'docsearch/surveys/form.html'
    fields = '__all__'


class SurveyUpdate(base_views.BaseUpdateView):
    model = models.Survey
    template_name = 'docsearch/surveys/form.html'
    fields = '__all__'


class SurveyDelete(base_views.BaseDeleteView):
    model = models.Survey
    template_name = 'docsearch/surveys/confirm_delete.html'


class SurveySearch(base_views.BaseSearchView):
    model = models.Survey
    template_name = 'docsearch/surveys/search.html'
    facet_fields = ['township_arr', 'range_arr', 'section_arr', 'map_number', 'location',
                    'job_number', 'number_of_sheets', 'date']
    facet_field_name_overrides = {'township_arr': 'township', 'section_arr': 'section',
                                  'range_arr': 'range'}
    sort_fields = ['township_arr', 'range_arr', 'section_arr', 'map_number_exact',
                   'location_exact', 'description_exact', 'job_number_exact',
                   'number_of_sheets_exact', 'date_exact']
