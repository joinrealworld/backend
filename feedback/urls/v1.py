from django.urls import path, include
from rest_framework import routers
from feedback import views

urlpatterns = [
    path('send/feedback', views.SendFeedbackAPIView.as_view(), name='send-feedback'),
    path('fetch/feedback', views.FetchFeedbackAPIView.as_view(), name='fetch-feedback'),
 ]