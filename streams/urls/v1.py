from django.urls import path, include
from rest_framework import routers
from streams import views

urlpatterns = [
    path('live-streams', views.live_streams_api, name='live-streams-api'),
	]