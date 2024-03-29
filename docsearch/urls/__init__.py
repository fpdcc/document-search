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
    path('login/', auth.views.LoginView.as_view(template_name='docsearch/login.html'), name='login'),
    path('logout/', auth.views.LogoutView.as_view(template_name='docsearch/logout.html'), name='logout'),
    path('reset_password/', views.PasswordResetView.as_view(template_name='docsearch/reset_password.html'), name='reset_password'),
    path('reset_password_sent/', auth.views.PasswordResetDoneView.as_view(template_name='docsearch/password_reset_sent.html'), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth.views.PasswordResetConfirmView.as_view(template_name='docsearch/password_reset_form.html'), name ='password_reset_confirm'),
    path('reset_password_complete/', auth.views.PasswordResetCompleteView.as_view(template_name='docsearch/password_reset_complete.html'), name ='password_reset_complete'),
    path('activity/', views.Activity.as_view(), name='activity'),
    path('activity/data/', views.ActivityData.as_view(), name='activity-data'),
    path('about/', views.About.as_view(), name='about'),
    path('pong/', views.pong),
]
