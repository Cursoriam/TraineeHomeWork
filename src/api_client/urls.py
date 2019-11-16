from django.urls import path

from src.api_client import views

urlpatterns: list = [
    path('client', views.ClientView.as_view())
]
