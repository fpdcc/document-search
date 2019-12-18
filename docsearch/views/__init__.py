from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.http import Http404

from docsearch import models
from .books import *
from .controlmonumentmaps import *
from .dossiers import *
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


def pong(request):
    """
    Zero-downtime deployment config function.
    """
    from django.http import HttpResponse

    try:
        from .deployment import DEPLOYMENT_ID
    except ImportError as e:
        return HttpResponse('Bad deployment: {}'.format(e), status=401)

    return HttpResponse(DEPLOYMENT_ID)
