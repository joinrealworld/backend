from django.urls import path, include
from raffel import views

urlpatterns = [
    path("checkout", views.RaffelCheckoutView.as_view(), name='raffel-checkout'),
    path("current_position", views.RaffelPositionAPIView.as_view(), name='raffel-position'),
    # path("join", views.JoinClanUsersView.as_view(), name='join-users'),
]