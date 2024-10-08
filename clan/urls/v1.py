from django.urls import path, include
from clan import views

urlpatterns = [
    path("users", views.FetchClanUsersView.as_view(), name='clan-users'),
    path("join", views.JoinClanUsersView.as_view(), name='join-users'),
]