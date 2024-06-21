from django.urls import path, include
from rest_framework import routers
from checklist.views import *

urlpatterns = [
    path('fetch/<slug:master_category>', FetchCheckListAPIView.as_view(), name='fetch-checklist'),
    path('submit', SubmitCheckListAPIView.as_view(), name='submit-checklist'),
    path('unselect', UnSelectCheckListAPIView.as_view(), name='unselect-checklist'),
    path('copy/checklist', CopyChecklistAPIView.as_view(), name='copy-checklist'),
	]