from docsearch import models
from . import base as base_views


class ProjectFileDetail(base_views.BaseDetailView):
    model = models.ProjectFile
    template_name = 'docsearch/projectfiles/detail.html'
    metadata_fields = ['area', 'section', 'job_number', 'job_name',
                       'description', 'cabinet_number', 'drawer_number',
                       'source_file']


class ProjectFileCreate(base_views.BaseCreateView):
    model = models.ProjectFile
    template_name = 'docsearch/projectfiles/form.html'
    fields = '__all__'


class ProjectFileUpdate(base_views.BaseUpdateView):
    model = models.ProjectFile
    template_name = 'docsearch/projectfiles/form.html'
    fields = '__all__'


class ProjectFileDelete(base_views.BaseDeleteView):
    model = models.ProjectFile
    template_name = 'docsearch/projectfiles/confirm_delete.html'
