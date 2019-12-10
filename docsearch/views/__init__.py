from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .books import *


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'docsearch/index.html'


class Search(LoginRequiredMixin, TemplateView):
    template_name = 'docsearch/search.html'
