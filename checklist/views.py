# Library Import
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import (
    GenericAPIView,
    UpdateAPIView,
    CreateAPIView,
    ListAPIView
)
from django.utils import timezone
import datetime
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,IsAdminUser,
)
from rest_framework.response import Response
from rest_framework.views import APIView
# Local Import
from polls.models import *
from user.permissions import (
    IsLoggedInUserOrAdmin,
    IsLoggedInUser,
)
from channel.serializers import *
from rest_framework.pagination import LimitOffsetPagination
from itertools import chain
from rest_framework.settings import api_settings
import random
from django.db.models import Q
import string
from constants.response import KEY_MESSAGE, KEY_PAYLOAD, KEY_STATUS
from constants.commons import handle_exceptions
from user.permissions import IsUserAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from checklist.serializers import *

class FetchCheckListAPIView(APIView):
	permission_classes = [IsUserAuthenticated]

	@handle_exceptions
	def get(self, request):
		master_checklist = MasterCheckList.objects.last()
		user_checklist = UserDailyCheckList.objects.filter(user = request.user).last()
		all_user_checklist = UserDailyCheckList.objects.all().order_by("-created_at")
		is_more_than_24_hours = False
		master_checklist = MasterCheckListSerializer(master_checklist).data
		selected_checklist_data = UserDailyCheckListSerializer(all_user_checklist, many=True).data
		res_data = []
		if user_checklist:
			current_time = timezone.now()
			time_difference = current_time - user_checklist.created_at
			if time_difference.total_seconds() > 24 * 3600:  # 24 hours in seconds
			    is_more_than_24_hours = True
			    res_data.append(master_checklist)
			else:
			    is_more_than_24_hours = False
		else:
		    is_more_than_24_hours = None
		return Response(
		    {
		        KEY_MESSAGE: "Success",
		        KEY_PAYLOAD: res_data+selected_checklist_data,
		        "is_more_than_24_hours": is_more_than_24_hours,
		        KEY_STATUS: 1,
		        "checklist_data": master_checklist
		    },
		    status=status.HTTP_200_OK
		)

class SubmitCheckListAPIView(APIView):
	permission_classes = [IsUserAuthenticated]

	@handle_exceptions
	def post(self, request):
		data = request.data.get('selected', None)
		selected_checklist = UserDailyCheckList.objects.create(selected = data, user = request.user)
		return Response(
		    {
		        KEY_MESSAGE: "Success",
		        KEY_PAYLOAD: "Checklist Submitted Successfully",
		        KEY_STATUS: 1
		    },
		    status=status.HTTP_200_OK
		)