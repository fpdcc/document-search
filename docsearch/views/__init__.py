import csv

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, TemplateView
from django.contrib.auth.views import PasswordResetView
from django_datatables_view.base_datatable_view import BaseDatatableView

from docsearch import models
from docsearch.templatetags.permissions import can_create
from .books import *
from .controlmonumentmaps import *
from .dossiers import *
from .deeptunnels import *
from .easements import *
from .flatdrawings import *
from .indexcards import *
from .licenses import *
from .projectfiles import *
from .rightsofway import *
from .surplusparcels import *
from .surveys import *
from .titles import *


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'docsearch/index.html'


class About(LoginRequiredMixin, TemplateView):
    template_name = 'docsearch/about.html'


class Activity(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = models.ActionLog
    context_object_name = 'actions'
    template_name = 'docsearch/activity.html'

    def test_func(self):
        # Only Read/Write users should be able to see this view
        return can_create(self.request.user)


class ActivityData(BaseDatatableView, UserPassesTestMixin):
    model = models.ActionLog
    columns = ['timestamp', 'user.username', 'action', 'content_type.model', 'object_id', 'content_object']
    order_columns = ['timestamp', 'user.username', 'action', 'content_type.model', 'object_id', '']
    max_display_length = 100

    def render_column(self, row, column):
        if column == 'timestamp':
            return row.timestamp.strftime("%B %-m, %Y, %-I:%M %p")
        elif column == 'content_object':
            return '<a href="{}">{}</a>'.format(
                row.content_object.get_absolute_url(),
                row.content_object
            ),
        else:
            return super().render_column(row, column)

    def test_func(self):
        # Only Read/Write users should be able to see this view
        return can_create(self.request.user)
    

class ExportData(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Serialize all License objects and return them as a downloadable CSV.
    """
    model = models.License
    permission_required = 'docsearch.view_license'
    fields = [
        'id', 'license_number', 'description', 'type', 'entity', 'diameter',
        'material', 'end_date', 'status', 'agreement_type', 'township',
        'range', 'section', 'geometry', 'source_file',
    ]
    array_fields = {'township', 'range', 'section'}
    choice_fields = {'type', 'status'}

    def get_header(self):
        return [
            str(self.model._meta.get_field(field).verbose_name).capitalize()
            if field != 'id' else 'ID'
            for field in self.fields
        ]

    def serialize_value(self, obj, field):
        value = getattr(obj, field)

        if value is None:
            return ''
        elif field in self.choice_fields:
            return getattr(obj, f'get_{field}_display')()
        elif field in self.array_fields:
            return ', '.join(str(v) for v in value if v is not None)
        elif field == 'geometry':
            return value.wkt
        elif field == 'source_file':
            return obj.source_file.url
        return value

    def serialize(self, obj):
        return [self.serialize_value(obj, field) for field in self.fields]

    def get(self, request, *args, **kwargs):
        filename = f'licenses-{timezone.localdate():%Y-%m-%d}.csv'
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        writer.writerow(self.get_header())
        for obj in self.model.objects.order_by('pk').iterator():
            writer.writerow(self.serialize(obj))

        return response


class PasswordResetView(PasswordResetView):
    email_template_name = 'docsearch/password_reset_email.html'


def pong(request):
    """
    Zero-downtime deployment config function.
    """
    from django.http import HttpResponse

    try:
        from ..deployment import DEPLOYMENT_ID
    except ImportError as e:
        return HttpResponse('Bad deployment: {}'.format(e), status=401)

    return HttpResponse(DEPLOYMENT_ID)
