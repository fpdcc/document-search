from django.urls import path

from docsearch import views

urlpatterns = [
    path('<int:pk>/', views.SurplusParcelDetail.as_view(), name="surplusparcel-detail"),
    path('create/', views.SurplusParcelCreate.as_view(), name="surplusparcel-create"),
    path('update/<int:pk>/', views.SurplusParcelUpdate.as_view(), name="surplusparcel-update"),
    path('delete/<int:pk>/', views.SurplusParcelDelete.as_view(), name="surplusparcel-delete"),
]
