from django.urls import path

from api_client import views

urlpatterns: list = [
    path('register', views.ClientView.as_view()),
    path('client/<str:login>', views.ClientViewToDelete.as_view()),
    path('authenticate', views.UserAuthenticate.as_view()),
    path('logout', views.UserLogoutView.as_view()),
    path('search', views.SearchView.as_view()),
    path('follow/<str:following_id>',
         views.FollowerView.as_view()),
    path('make_pitt', views.CreatePittView.as_view()),
    path('pitts/<str:pitt_id>', views.DeletePittView.as_view()),
    path('feed/page=<int:page>', views.FeedView.as_view()),
    path('list', views.ClientListView.as_view()),
]
