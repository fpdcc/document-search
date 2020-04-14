import re

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from haystack.generic_views import FacetedSearchView
from django_datatables_view.base_datatable_view import BaseDatatableView

from docsearch import models, forms, query


class DocumentPermissionRequiredMixin(PermissionRequiredMixin):
    permission_action = None

    def get_permission_required(self):
        """
        Override ths method to allow base classes to specify default permissions
        based on the specific models that those base classes are concerned with.
        """
        if self.permission_required is None:
            if not self.permission_action:
                raise NotImplementedError(
                    '{} is missing the permission_required '
                    'attribute.'.format(self.__class__.__name__)
                )
            return [
                '{app}.{action}_{model}'.format(
                    app=self.model._meta.app_label,
                    action=self.permission_action,
                    model=self.model.get_slug()
                )
            ]
        else:
            return super().get_permission_required()


class BaseCreateView(LoginRequiredMixin, DocumentPermissionRequiredMixin, CreateView):
    permission_action = 'add'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['cancel_url'] = self.get_cancel_url()
        return context

    def get_cancel_url(self):
        return self.model.get_search_url()

    def form_valid(self, form):
        # Generate the response before saving an ActionLog entry, since the
        # ActionLog requires an object to have been saved to the database
        response = super().form_valid(form)
        models.ActionLog.objects.create(
            user=self.request.user,
            content_object=form.instance,
            action=models.ActionLog.Action.CREATE
        )
        return response


class BaseUpdateView(LoginRequiredMixin, DocumentPermissionRequiredMixin, UpdateView):
    permission_action = 'change'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['cancel_url'] = self.get_cancel_url(obj=context['object'])
        context['delete_url'] = self.get_delete_url(obj=context['object'])
        return context

    def get_cancel_url(self, obj):
        return obj.get_absolute_url()

    def get_delete_url(self, obj):
        return obj.get_delete_url()

    def form_valid(self, form):
        models.ActionLog.objects.create(
            user=self.request.user,
            content_object=form.instance,
            action=models.ActionLog.Action.UPDATE
        )
        return super().form_valid(form)


class BaseDetailView(LoginRequiredMixin, DocumentPermissionRequiredMixin, DetailView):
    array_fields = []
    permission_action = 'view'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['update_url'] = self.get_update_url(obj=context['object'])
        return context

    def get_update_url(self, obj):
        return obj.get_update_url()


class BaseDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    def has_permission(self):
        # Only Staff users should be able to delete
        return self.request.user.is_staff

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['cancel_url'] = self.get_cancel_url(obj=context['object'])
        return context

    def get_cancel_url(self, obj):
        return obj.get_absolute_url()

    def get_success_url(self):
        return self.model.get_search_url()


class BaseSearchView(LoginRequiredMixin, DocumentPermissionRequiredMixin, FacetedSearchView):
    form_class = forms.BaseSearchForm
    queryset = query.FuzzySearchQuerySet()
    template_name = 'docsearch/search.html'
    permission_action = 'view'
    sort_fields = []
    geo_facet_fields = [
        'area', 'section', 'section_arr', 'township', 'township_arr',
        'range', 'range_arr',
    ]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['parameters'] = self.request.GET.copy()
        context['selected_facets'] = self.request.GET.getlist('selected_facets', [])
        context['selected_facet_fields'] = set([facet.split(':')[0] for facet in
                                                context['selected_facets']])

        context['selected_facet_map'] = {facet: [] for facet in
                                         context['selected_facet_fields']}
        for facet in context['selected_facets']:
            key, val = facet.split(':')
            context['selected_facet_map'][key].append(val)

        context['sort'] = self.request.GET.get('sort')
        context['sortdir'] = self.request.GET.get('sortdir')
        return context

    def form_valid(self, form):
        form.cleaned_data['models'] = [self.model._meta.label]
        return super().form_valid(form)

    def get_queryset(self):
        sqs = super().get_queryset().models(self.model)
        for facet_field in self.facet_fields:
            # Sort facet options alphabetically, not by hit count
            sqs = sqs.facet(facet_field, sort='index')
        sort = self._get_sort()
        if sort:
            sqs = sqs.order_by(sort)
        return sqs

    def _get_sort(self):
        """
        Extract the 'sort' parameter from the URL if it's valid; otherwise,
        suppress it by returning None.
        """
        sort = self.request.GET.get('sort')
        if sort and sort in self.sort_fields:
            sortdir = self.request.GET.get('sortdir')
            return f'-{sort}' if sortdir == 'desc' else sort
        else:
            return None

    def get_sort_options(self):
        # We may eventually need a specialized data structure to store
        # the values and labels of sort fields, but for now the
        # conversion rule is pretty simple
        sort_options = []
        for sort_field in self.sort_fields:
            label = sort_field
            replacements = [
                ('_exact$', ''),
                ('_arr$', ''),
                ('_', ' ')
            ]
            for pattern, new_pattern in replacements:
                label = re.sub(pattern, new_pattern, label)
            sort_options.append({'value': sort_field, 'label': label})
        return sort_options


class BaseDocumentData(BaseDatatableView, DocumentPermissionRequiredMixin):
    model = models.ActionLog
    document_model = None  # Children must set this attribute
    permission_action = 'view'
    columns = ['timestamp', 'user.username', 'action']
    order_columns = ['timestamp', 'user.username', 'action']
    max_display_length = 100

    def render_column(self, row, column):
        if column == 'timestamp':
            return row.timestamp.strftime("%B %-m, %Y, %-I:%M %p")
        else:
            return super().render_column(row, column)

    def filter_queryset(self, qs):
        if self.document_model is None:
            raise NotImplementedError(
                'Child classes must implement the document_model attribute'
            )
        else:
            content_type = ContentType.objects.get_for_model(self.document_model)
            qs = qs.filter(content_type=content_type)
            return super().filter_queryset(qs)
