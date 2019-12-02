from django.urls import path

from api_client import views

urlpatterns: list = [
    path('register', views.ClientView.as_view()),
    path('client/<str:login>', views.ClientViewToDelete.as_view()),
    path('authenticate', views.UserAuthenticate.as_view()),
    path('authorize', views.UserAutorization.as_view()),
    path('<str:id>/followings', views.GetFollowersView.as_view()),
    path('<str:follower_id>/follow/<str:user_id>',
         views.FollowerView.as_view()),
    path('<str:id>/make_pitt', views.FollowerView.as_view()),
    path('<str:login>/pitts/<pitt:id>', views.DeletePittView.as_view()),
    path('<str:login>/feed/page=<int: page>', views.FeedView.as_view()),
]
