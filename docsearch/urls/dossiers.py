from django.urls import path

from docsearch import views

urlpatterns = [
    path('<int:pk>/', views.DossierDetail.as_view(), name="dossier-detail"),
    path('create/', views.DossierCreate.as_view(), name="dossier-create"),
    path('update/<int:pk>/', views.DossierUpdate.as_view(), name="dossier-update"),
    path('delete/<int:pk>/', views.DossierDelete.as_view(), name="dossier-delete"),
]
