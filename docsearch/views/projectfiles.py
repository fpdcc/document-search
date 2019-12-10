from django.urls import reverse_lazy

from docsearch import models
from . import base as base_views


class ProjectFileDetail(base_views.BaseDetailView):
    model = models.ProjectFile
    template_name = 'docsearch/projectfiles/detail.html'
    update_url_from_obj = 'projectfile-update'
    metadata_fields = ['area', 'section', 'job_number', 'job_name',
                       'description', 'cabinet_number', 'drawer_number',
                       'source_file']


class ProjectFileCreate(base_views.BaseCreateView):
    model = models.ProjectFile
    template_name = 'docsearch/projectfiles/form.html'
    fields = '__all__'
    cancel_url = reverse_lazy('search', args=('projectfiles',))


class ProjectFileUpdate(base_views.BaseUpdateView):
    model = models.ProjectFile
    template_name = 'docsearch/projectfiles/form.html'
    fields = '__all__'
    cancel_url_from_obj = 'projectfile-detail'
    delete_url_from_obj = 'projectfile-delete'


class ProjectFileDelete(base_views.BaseDeleteView):
    model = models.ProjectFile
    template_name = 'docsearch/projectfiles/confirm_delete.html'
    cancel_url_from_obj = 'projectfile-detail'
    success_url = reverse_lazy('search', args=('projectfiles',))
