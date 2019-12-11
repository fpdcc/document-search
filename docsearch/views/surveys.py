from docsearch import models
from . import base as base_views


class SurveyDetail(base_views.BaseDetailView):
    model = models.Survey
    template_name = 'docsearch/surveys/detail.html'
    metadata_fields = ['area', 'section', 'map_number', 'location',
                       'description', 'job_number', 'number_of_sheets',
                       'date', 'cross_ref_area', 'cross_ref_section',
                       'cross_ref_map_number', 'source_file']


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