from django.urls import path, include
from rest_framework import routers
from payment import views

urlpatterns = [
    path('create_customer', views.CreateCustomerAPIView.as_view(), name='create-stripe-customer'),
    path('create_card', views.CreateCustomerCardAPIView.as_view(), name='create-stripe-card'),
    
]