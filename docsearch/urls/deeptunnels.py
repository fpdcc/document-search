from django.urls import path

from docsearch import views

urlpatterns = [
    path('<int:pk>/', views.DeepTunnelDetail.as_view(), name="deeptunnel-detail"),
    path('create/', views.DeepTunnelCreate.as_view(), name="deeptunnel-create"),
    path('search/', views.DeepTunnelSearch.as_view(), name="deeptunnel-search"),
    path('data/', views.DeepTunnelData.as_view(), name="deeptunnel-data"),
    path('update/<int:pk>/', views.DeepTunnelUpdate.as_view(), name="deeptunnel-update"),
    path('delete/<int:pk>/', views.DeepTunnelDelete.as_view(), name="deeptunnel-delete"),
]
