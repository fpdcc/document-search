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
from django.urls import path

from docsearch import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('book/<int:pk>/', views.BookDetail.as_view(), name="book"),
    path('book/create/', views.BookCreate.as_view(), name="book-create"),
    path('book/update/<int:pk>/', views.BookUpdate.as_view(), name="book-update"),
    path('book/delete/<int:pk>/', views.BookDelete.as_view(), name="book-delete"),
    path('admin/', admin.site.urls),
    path('logout/', auth.views.LogoutView.as_view(), name='logout'),
]
