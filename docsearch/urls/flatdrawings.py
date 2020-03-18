from django.urls import path

from docsearch import views

urlpatterns = [
    path('<int:pk>/', views.FlatDrawingDetail.as_view(), name="flatdrawing-detail"),
    path('create/', views.FlatDrawingCreate.as_view(), name="flatdrawing-create"),
    path('search/', views.FlatDrawingSearch.as_view(), name="flatdrawing-search"),
    path('data/', views.FlatDrawingData.as_view(), name="flatdrawing-data"),
    path('update/<int:pk>/', views.FlatDrawingUpdate.as_view(), name="flatdrawing-update"),
    path('delete/<int:pk>/', views.FlatDrawingDelete.as_view(), name="flatdrawing-delete"),
]
