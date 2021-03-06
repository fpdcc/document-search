from django.urls import path

from docsearch import views

urlpatterns = [
    path('<int:pk>/', views.ControlMonumentMapDetail.as_view(), name="controlmonumentmap-detail"),
    path('create/', views.ControlMonumentMapCreate.as_view(), name="controlmonumentmap-create"),
    path('search/', views.ControlMonumentMapSearch.as_view(), name="controlmonumentmap-search"),
    path('data/', views.ControlMonumentMapData.as_view(), name="controlmonumentmap-data"),
    path('update/<int:pk>/', views.ControlMonumentMapUpdate.as_view(), name="controlmonumentmap-update"),
    path('delete/<int:pk>/', views.ControlMonumentMapDelete.as_view(), name="controlmonumentmap-delete"),
]
