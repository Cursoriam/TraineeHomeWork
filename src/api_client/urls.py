from django.urls import path

from api_client import views

urlpatterns: list = [
    path('client', views.ClientView.as_view()),
    path('client/<str:id>', views.ClientViewToDelete.as_view()),
]
