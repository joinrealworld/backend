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
from datetime import datetime, date
from checklist.management.commands.scheduler import *

class FetchCheckListAPIView(APIView):
	permission_classes = [IsUserAuthenticated]

	@handle_exceptions
	def get(self, request, master_category):
		user_daily_checklist = UserDailyCheckList.objects.filter(master_category__uuid=master_category).order_by('id')
		return Response(
		    {
		        KEY_MESSAGE: "Success",
		        KEY_PAYLOAD: UserDailyCheckListSerializer(user_daily_checklist, many=True).data,
		       
		    },
		    status=status.HTTP_200_OK
		)


class SubmitCheckListAPIView(APIView):
	permission_classes = [IsUserAuthenticated]

	@handle_exceptions
	def post(self, request):
		data = request.data.get('selected', None)
		user_checklist = request.data.get('user_checklist', None)
		user_checklist = UserDailyCheckList.objects.get(uuid=user_checklist)
		selected_checklist = DailyChecked.objects.create(checklist=user_checklist, user = request.user,  selected = data)
		return Response(
		    {
		        KEY_MESSAGE: "Success",
		        KEY_PAYLOAD: "Checklist Submitted Successfully",
		        KEY_STATUS: 1
		    },
		    status=status.HTTP_200_OK
		)

class CopyChecklistAPIView(APIView):
	permission_classes = []

	@handle_exceptions
	def get(self, request):
		create_copy_daily_checklist()
		return Response(
		    {
		        KEY_MESSAGE: "Success",
		        KEY_PAYLOAD: "Checklist Copied Successfully",
		        KEY_STATUS: 1
		    },
		    status=status.HTTP_200_OK
		)

class UnSelectCheckListAPIView(APIView):
	permission_classes = []

	@handle_exceptions
	def post(self, request):
		check_id = request.data.get("check_id", None)
		DailyChecked.objects.get(uuid=check_id).delete()
		return Response(
		    {
		        KEY_MESSAGE: "Success",
		        KEY_PAYLOAD: "Unselected Successfully",
		        KEY_STATUS: 1
		    },
		    status=status.HTTP_200_OK
		)

class CheckListOptionsAPIView(APIView):
	permission_classes = [IsUserAuthenticated]

	@handle_exceptions
	def get(self, request):
		check_id = request.data.get("check_id", None)
		master_checklist = MasterCheckList.objects.last()
		return Response(
		    {
		        KEY_MESSAGE: "Success",
		        KEY_PAYLOAD: master_checklist.options.split(','),
		        KEY_STATUS: 1
		    },
		    status=status.HTTP_200_OK
		)
