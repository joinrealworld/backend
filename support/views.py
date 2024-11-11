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
from user.permissions import (
    IsLoggedInUserOrAdmin,
    IsLoggedInUser,
)
# from feedback.serializers import *
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
from user.serializers import UserSimpleSerializer
from user.models import User
from django.utils.timezone import make_aware
from support.serializers import *
from support.models import *
from rest_framework.decorators import action

class SendMessageAPIView(APIView):
	permission_classes = [IsUserAuthenticated]

	@handle_exceptions
	def post(self, request, support_chat_id=None):
		support_chat_id = request.query_params.get('support_chat_id', None)
		data = request.data.get("message", None)
		user = request.user

        # Validate each message in the list
		for message in data:
		    content = data.get("content", "").strip()  # Use strip to check for empty spaces
		    timestamp = data.get("timestamp", None)

		    # Check if content is provided and not empty
		    if not content:
		        return Response(
		            status=status.HTTP_400_BAD_REQUEST,
		            data={
						KEY_MESSAGE: "Message content cannot be empty.",
						KEY_PAYLOAD: SupportSerializer(support_chat).data,
						KEY_STATUS: 0,   
		            },
		        )

		    # Check if timestamp is provided and valid
		    if not timestamp:
		        return Response(
		            status=status.HTTP_400_BAD_REQUEST,
					data={
						KEY_MESSAGE: "Message timestamp cannot be empty.",
						KEY_PAYLOAD: SupportSerializer(support_chat).data,
						KEY_STATUS: 0,   
					},
		        )

		if support_chat_id is not None: # admin sedning the msg
			support_chat = Support.objects.get(uuid=support_chat_id)
		else: # user sending the msg
			support_chat, created = Support.objects.get_or_create(user=user)
			
		messages = support_chat.messages
		data["sender"] = UserSimpleSerializer(user).data
		messages.append(data)
		support_chat.messages = messages
		support_chat.save()
        

		return Response(
		    status=status.HTTP_201_CREATED,
		    data={
		    	KEY_MESSAGE: "Message added successfully.",
	            KEY_PAYLOAD: SupportSerializer(support_chat).data,
	            KEY_STATUS: 1,
		    },
		)

class FetchMessageAPIView(APIView):
	permission_classes = [IsUserAuthenticated]

	@handle_exceptions
	def get(self, request):
		# support chat id will be None in case if normal user is calling
		support_chat_id = request.query_params.get('support_chat_id', None)
		user = request.user
		if support_chat_id is None:
			support_chat, created = Support.objects.get_or_create(user=user)
		else:
			if user.is_admin==True or user.is_super_admin == True:
				support_chat = Support.objects.get(uuid = support_chat_id)
			else:
				support_chat = Support.objects.get(user = user)
		return Response(
		    status=status.HTTP_200_OK,
		    data={
			    KEY_MESSAGE: "Message Fetched successfully.",
	            KEY_PAYLOAD: SupportSerializer(support_chat).data,
	            KEY_STATUS: 1,
		    },
		)


class SupportUserListAPIView(APIView):
	permission_classes = [IsLoggedInUserOrAdmin]

	@handle_exceptions
	def get(self, request):
		support = Support.objects.all()
		return Response(
		    status=status.HTTP_200_OK,
		    data={
			    KEY_MESSAGE: "Support User List Fetched successfully.",
	            KEY_PAYLOAD: SupportUserListSerializer(support, many=True).data,
	            KEY_STATUS: 1,
		    },
		)





