from django.urls import path, include
from rest_framework import routers
from support import views

urlpatterns = [
    path('send_message/<uuid:support_chat_id>', views.SendMessageAPIView.as_view(), name='send-support-message'),
    path('fetch_message', views.FetchMessageAPIView.as_view(), name='fetch-support-message'),
    path('support_list', views.SupportUserListAPIView.as_view(), name='support-user-list')    
	]