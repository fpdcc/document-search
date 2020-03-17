from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, TemplateView

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


class Activity(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = models.ActionLog
    context_object_name = 'actions'
    template_name = 'docsearch/activity.html'

    def test_func(self):
        # Only Read/Write users should be able to see this view.
        return can_create(self.request.user)


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
