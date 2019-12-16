from django.urls import path

from docsearch import views

urlpatterns = [
    path('<int:pk>/', views.ProjectFileDetail.as_view(), name="projectfile-detail"),
    path('create/', views.ProjectFileCreate.as_view(), name="projectfile-create"),
    path('search/', views.ProjectFileSearch.as_view(), name="projectfile-search"),
    path('update/<int:pk>/', views.ProjectFileUpdate.as_view(), name="projectfile-update"),
    path('delete/<int:pk>/', views.ProjectFileDelete.as_view(), name="projectfile-delete"),
]
