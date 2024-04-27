from django.urls import path, include
from rest_framework import routers
from checklist.views import *

urlpatterns = [
    path('fetch', FetchCheckListAPIView.as_view(), name='fetch-checklist'),
    path('submit', SubmitCheckListAPIView.as_view(), name='submit-checklist'),
    # path('poll-list', PollListAPIView.as_view(), name='poll-list'),
    # path('answer-poll', AnswerPollAPIView.as_view(), name='answer-poll'),
	]