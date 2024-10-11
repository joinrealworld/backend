from django.urls import path, include
from raffel import views

urlpatterns = [
    path("checkout", views.RaffelCheckoutView.as_view(), name='raffel-checkout'),
    # path("join", views.JoinClanUsersView.as_view(), name='join-users'),
]