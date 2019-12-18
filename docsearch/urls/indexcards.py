from django.urls import path

from docsearch import views

urlpatterns = [
    path('<int:pk>/', views.IndexCardDetail.as_view(), name="indexcard-detail"),
    path('create/', views.IndexCardCreate.as_view(), name="indexcard-create"),
    path('search/', views.IndexCardSearch.as_view(), name="indexcard-search"),
    path('update/<int:pk>/', views.IndexCardUpdate.as_view(), name="indexcard-update"),
    path('delete/<int:pk>/', views.IndexCardDelete.as_view(), name="indexcard-delete"),
]
