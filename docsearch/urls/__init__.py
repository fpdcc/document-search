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

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('books/', include(books_patterns)),
    path('controlmonumentmaps/', include(controlmonumentmaps_patterns)),
    path('admin/', admin.site.urls),
    path('logout/', auth.views.LogoutView.as_view(), name='logout'),
]
