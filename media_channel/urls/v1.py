from django.urls import path, include
from rest_framework import routers
from media_channel import views

urlpatterns = [
    path('send/message', views.SendMessageAPIView.as_view(), name='send-message'),
    path('fetch/message', views.FetchMessagesAPIView.as_view(), name='fetch-message'),
    path('like/message', views.LikeMessagesAPIView.as_view(), name='like-message'),
    path('notifications', views.NotificationsAPIView.as_view(), name='notifications'),
 ]