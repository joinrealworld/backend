from django.urls import path, include
from rest_framework import routers
from blackhall import views

urlpatterns = [
    path('send/message', views.SendMessageAPIView.as_view(), name='send-message'),
 ]