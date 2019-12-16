from django.urls import path

from docsearch import views

urlpatterns = [
    path('<int:pk>/', views.TitleDetail.as_view(), name="title-detail"),
    path('create/', views.TitleCreate.as_view(), name="title-create"),
    path('search/', views.TitleSearch.as_view(), name="title-search"),
    path('update/<int:pk>/', views.TitleUpdate.as_view(), name="title-update"),
    path('delete/<int:pk>/', views.TitleDelete.as_view(), name="title-delete"),
]
