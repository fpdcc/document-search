from django.urls import path

from docsearch import views

urlpatterns = [
    path('<int:pk>/', views.SurveyDetail.as_view(), name="survey-detail"),
    path('create/', views.SurveyCreate.as_view(), name="survey-create"),
    path('search/', views.SurveySearch.as_view(), name="survey-search"),
    path('data/', views.SurveyData.as_view(), name="survey-data"),
    path('update/<int:pk>/', views.SurveyUpdate.as_view(), name="survey-update"),
    path('delete/<int:pk>/', views.SurveyDelete.as_view(), name="survey-delete"),
]
