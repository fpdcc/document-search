"""docsearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin, auth
from django.urls import path, include

from docsearch import views
from .books import urlpatterns as books_patterns
from .controlmonumentmaps import urlpatterns as controlmonumentmaps_patterns
from .dossiers import urlpatterns as dossiers_patterns
from .deeptunnels import urlpatterns as deeptunnels_patterns
from .easements import urlpatterns as easements_patterns
from .flatdrawings import urlpatterns as flatdrawings_patterns
from .indexcards import urlpatterns as indexcards_patterns
from .licenses import urlpatterns as licenses_patterns
from .projectfiles import urlpatterns as projectfiles_patterns
from .rightsofway import urlpatterns as rightsofway_patterns
from .surplusparcels import urlpatterns as surplusparcels_patterns
from .surveys import urlpatterns as surveys_patterns
from .titles import urlpatterns as titles_patterns

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('books/', include(books_patterns)),
    path('controlmonumentmaps/', include(controlmonumentmaps_patterns)),
    path('dossiers/', include(dossiers_patterns)),
    path('deeptunnels/', include(deeptunnels_patterns)),
    path('easements/', include(easements_patterns)),
    path('flatdrawings/', include(flatdrawings_patterns)),
    path('indexcards/', include(indexcards_patterns)),
    path('licenses/', include(licenses_patterns)),
    path('projectfiles/', include(projectfiles_patterns)),
    path('rightsofway/', include(rightsofway_patterns)),
    path('surplusparcels/', include(surplusparcels_patterns)),
    path('surveys/', include(surveys_patterns)),
    path('titles/', include(titles_patterns)),
    path('admin/', admin.site.urls),
    path('logout/', auth.views.LogoutView.as_view(), name='logout'),
    path('pong/', views.pong),
]
