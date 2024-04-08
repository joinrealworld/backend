from django.urls import path, include
from rest_framework import routers
from payment import views

urlpatterns = [
    path('create_customer', views.CreateCustomerAPIView.as_view(), name='create-stripe-customer'),
    path('create_card', views.CreateCustomerCardAPIView.as_view(), name='create-stripe-card'),
    path('fetch_prices', views.FetchSubscriptionsAPIView.as_view(), name='fetch-stripe-prices'),
    path('create_subscription', views.CreateSubscriptionAPIView.as_view(), name='create-stripe-subscription'),
    path('retrive_subscription', views.RetriveSubscriptionAPIView.as_view(), name='retrive-stripe-subscription'),
    path('cancle_subscription', views.CancleSubscriptionAPIView.as_view(), name='cancle-stripe-subscription'),
    path('card_list', views.CustomerCardListAPIView.as_view(), name='customer-card-list'),
    path('create_card_token', views.CustomerCardTokenAPIView.as_view(), name='customer-card-token'),
    path('fetch/<str:entity>/customer', views.FetchAllStripeCustomerAPIView.as_view(), name='fetch-stripe-customer'),
    
]