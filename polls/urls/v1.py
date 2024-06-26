from django.urls import path, include
from rest_framework import routers
from polls.views import *

urlpatterns = [
    path('create_poll', CreatePollAPIView.as_view(), name='create-poll'),
    path('poll-list/<slug:master_category>', PollListAPIView.as_view(), name='poll-list'),
    path('answer-poll', AnswerPollAPIView.as_view(), name='answer-poll'),
	]