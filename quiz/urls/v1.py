from django.urls import path, include
from rest_framework import routers
from quiz.views import *

urlpatterns = [
    path('status', SendQuizStatusAPIView.as_view(), name='send-quiz-status'),
	]