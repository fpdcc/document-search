from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.http import Http404

from docsearch import models
from .books import *
from .controlmonumentmaps import *


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'docsearch/index.html'


class Search(LoginRequiredMixin, TemplateView):
    template_name = 'docsearch/search.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['model'] = self._get_model(kwargs)
        return context

    def _get_model(self, kwargs):
        if not kwargs.get('doctype'):
            raise ValueError('doctype is a required kwarg')
        try:
            return models.get_model_from_slug(kwargs['doctype'])
        except models.InvalidSlugException as e:
            raise Http404(str(e))
