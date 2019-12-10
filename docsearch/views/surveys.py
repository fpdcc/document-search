from django.urls import reverse_lazy

from docsearch import models
from . import base as base_views


class SurveyDetail(base_views.BaseDetailView):
    model = models.Survey
    template_name = 'docsearch/surveys/detail.html'
    update_url_from_obj = 'survey-update'
    metadata_fields = ['area', 'section', 'map_number', 'location',
                       'description', 'job_number', 'number_of_sheets',
                       'date', 'cross_ref_area', 'cross_ref_section',
                       'cross_ref_map_number', 'source_file']


class SurveyCreate(base_views.BaseCreateView):
    model = models.Survey
    template_name = 'docsearch/surveys/form.html'
    fields = '__all__'
    cancel_url = reverse_lazy('search', args=('surveys',))


class SurveyUpdate(base_views.BaseUpdateView):
    model = models.Survey
    template_name = 'docsearch/surveys/form.html'
    fields = '__all__'
    cancel_url_from_obj = 'survey-detail'
    delete_url_from_obj = 'survey-delete'


class SurveyDelete(base_views.BaseDeleteView):
    model = models.Survey
    template_name = 'docsearch/surveys/confirm_delete.html'
    cancel_url_from_obj = 'survey-detail'
    success_url = reverse_lazy('search', args=('surveys',))
