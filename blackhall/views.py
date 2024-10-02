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
from blackhall.models import *
from user.permissions import (
    IsLoggedInUserOrAdmin,
    IsLoggedInUser,
)
from blackhall.serializers import *
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
from blackhall.serializers import *

class SendMessageAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def post(self, request):
        content = request.data.get("content", None)
        today = make_aware(datetime.now()).date()
        user = request.user
        message_exists = BlackhallChat.objects.filter(user=user, timestamp__date=today).exists()

        if message_exists:
            return Response(
                status=status.HTTP_200_OK,
                data={
                    KEY_MESSAGE: "You have already sent a message today. Please try again tomorrow.",
                    KEY_PAYLOAD: "Success",
                    KEY_STATUS: 0
                },
            )
        chat = BlackhallChat.objects.create(
            user=user,
            timestamp=today,
            message = content,
        )
        user.coin = user.coin+50
        user.save()
        print(user.coin)
        return Response(
                status=status.HTTP_200_OK,
                data={
                    KEY_MESSAGE: "category data sent successfully.",
                    KEY_PAYLOAD: "Success", #MasterCategorySerializer(category, many = True, context=context).data,
                    KEY_STATUS: 1
                },
            )

class FetchMessagesAPIView(APIView):
	permission_classes = [IsUserAuthenticated]

	@handle_exceptions
	def get(self, request):
		user = request.user
		# Get today's date
		today = make_aware(datetime.now()).date()

		# Retrieve today's chat messages for the user
		try:
		    chat = BlackhallChat.objects.filter(timestamp__date=today)
		except BlackhallChat.DoesNotExist:
		    return Response(
		        status=status.HTTP_404_NOT_FOUND,
		        data={
		            "message": "No messages found for today.",
		            "status": 0
		        },
		    )

		return Response(
		    status=status.HTTP_200_OK,
		    data={
		        "message": "Messages retrieved successfully.",
		        "status": 1,
		        "data": BlackHallSerializer(chat, many=True).data  # Returning the list of messages
		    },
		)