from django.urls import path

from docsearch import views

urlpatterns = [
    path('<int:pk>/', views.BookDetail.as_view(), name="book-detail"),
    path('create/', views.BookCreate.as_view(), name="book-create"),
    path('search/', views.BookSearch.as_view(), name="book-search"),
    path('update/<int:pk>/', views.BookUpdate.as_view(), name="book-update"),
    path('delete/<int:pk>/', views.BookDelete.as_view(), name="book-delete"),
]
