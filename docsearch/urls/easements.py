from django.urls import path

from docsearch import views

urlpatterns = [
    path('<int:pk>/', views.EasementDetail.as_view(), name="easement-detail"),
    path('create/', views.EasementCreate.as_view(), name="easement-create"),
    path('update/<int:pk>/', views.EasementUpdate.as_view(), name="easement-update"),
    path('delete/<int:pk>/', views.EasementDelete.as_view(), name="easement-delete"),
]
