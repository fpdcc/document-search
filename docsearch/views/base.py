from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from haystack.generic_views import FacetedSearchView

from docsearch import models, forms


class BaseCreateView(LoginRequiredMixin, CreateView):
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


class BaseUpdateView(LoginRequiredMixin, UpdateView):
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


class BaseDetailView(LoginRequiredMixin, DetailView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['update_url'] = self.get_update_url(obj=context['object'])
        return context

    def get_update_url(self, obj):
        return obj.get_update_url()


class BaseDeleteView(LoginRequiredMixin, DeleteView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['cancel_url'] = self.get_cancel_url(obj=context['object'])
        return context

    def get_cancel_url(self, obj):
        return obj.get_absolute_url()

    def get_success_url(self):
        return self.model.get_search_url()


class BaseSearchView(LoginRequiredMixin, FacetedSearchView):
    form_class = forms.BaseSearchForm
    template_name = 'docsearch/search.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['parameters'] = self.request.GET.copy()
        context['selected_facets'] = self.request.GET.getlist('selected_facets', [])
        context['selected_facet_fields'] = set([facet.split(':')[0] for facet in
                                                context['selected_facets']])
        return context

    def form_valid(self, form):
        form.cleaned_data['models'] = [self.model._meta.label]
        return super().form_valid(form)

    def get_queryset(self):
        return super().get_queryset().models(self.model)
