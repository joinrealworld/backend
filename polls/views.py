# Library Import
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import (
    GenericAPIView,
    UpdateAPIView,
    CreateAPIView,
    ListAPIView
)
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
from datetime import datetime, timedelta, date
import string
from constants.response import KEY_MESSAGE, KEY_PAYLOAD, KEY_STATUS
from constants.commons import handle_exceptions
from user.permissions import IsUserAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from polls.serializers import *
# Create your views here.

class CreatePollAPIView(APIView):
	permission_classes = [IsLoggedInUserOrAdmin]

	@handle_exceptions
	def post(self, request):
		serializer = CreatePollSerializer(data=request.data)
		if not serializer.is_valid():
		    errors = serializer.errors
		    return Response(
		        {
		            KEY_MESSAGE: "Validation Error",
		            KEY_PAYLOAD: errors,
		            KEY_STATUS: 0
		        },
		        status=status.HTTP_400_BAD_REQUEST
		    )

		question = serializer.validated_data.get("question")
		options = serializer.validated_data.get("options")
		master_poll_quetion = MasterPollQuetion.objects.create(quetion = question)
		for opt in options:
			master_poll_option = MasterPollOption.objects.create(poll_quetion = master_poll_quetion, option = opt)

		return Response(
		    {
		        KEY_MESSAGE: "Success",
		        KEY_PAYLOAD: "Poll Created Successfully",
		        KEY_STATUS: 1
		    },
		    status=status.HTTP_200_OK
		)

class PollListAPIView(APIView):
	permission_classes = [IsUserAuthenticated]

	@handle_exceptions
	def get(self, request):
		master_poll_quetion = MasterPollQuetion.objects.all().order_by("created_at")
		return Response(
		    {
		        KEY_MESSAGE: "Success",
		        KEY_PAYLOAD: MasterPollQuetionSerializer(master_poll_quetion, many=True).data,
		        KEY_STATUS: 1
		    },
		    status=status.HTTP_200_OK
		)

class AnswerPollAPIView(APIView):
	permission_classes = [IsUserAuthenticated]

	@handle_exceptions
	def post(self, request):
		serializer = AnswerPollSerializer(data=request.data)

		if not serializer.is_valid():
			errors = serializer.errors
			return Response(
			    {
					KEY_MESSAGE: "Validation Error",
					KEY_PAYLOAD: errors,
					KEY_STATUS: 0
			    },
				status=status.HTTP_400_BAD_REQUEST
			)

		question_id = serializer.validated_data.get('question_id')
		selected_option_id = serializer.validated_data.get('selected_option_id')
		obj, created = UserPoll.objects.get_or_create(poll_quetion = MasterPollQuetion.objects.get(uuid = question_id), user = request.user)
		obj.selected_option = MasterPollOption.objects.get(uuid = selected_option_id)
		obj.is_checked = True
		obj.save()
		return Response(
		    {
		        KEY_MESSAGE: "Success",
		        KEY_PAYLOAD: "Answer processed successfully.",
		        KEY_STATUS: 1
		    },
		    status=status.HTTP_200_OK
		)

# class FetchDailyCheckListAPIView(APIView):
# 	permission_classes = [IsUserAuthenticated]

# 	@handle_exceptions
# 	def post(self, request):
# 		serializer = AnswerPollSerializer(data=request.data)

# 		if not serializer.is_valid():
# 			errors = serializer.errors
# 			return Response(
# 				{
# 					KEY_MESSAGE: "Validation Error",
# 					KEY_PAYLOAD: errors,
# 					KEY_STATUS: 0
# 				},
# 				status=status.HTTP_400_BAD_REQUEST
# 			)

# 		question_id = serializer.validated_data.get('question_id')
# 		selected_option_id = serializer.validated_data.get('selected_option_id')
# 		obj, created = UserPoll.objects.get_or_create(poll_quetion = MasterPollQuetion.objects.get(uuid = question_id), user = request.user)
# 		obj.selected_option = MasterPollOption.objects.get(uuid = selected_option_id)
# 		obj.is_checked = True
# 		obj.save()
# 		return Response(
# 			{
# 				KEY_MESSAGE: "Success",
# 				KEY_PAYLOAD: "Answer processed successfully.",
# 				KEY_STATUS: 1
# 			},
# 			status=status.HTTP_200_OK
# 		)







