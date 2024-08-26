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


class SendMessageAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def post(self, request):
        data = request.data.get("data", None)
        today = make_aware(datetime.now()).date()
        user = request.user
        # Check if there is already a chat object for today
        chat, created = BlackhallChat.objects.get_or_create(
            user=user,
            timestamp__date=today,
            defaults={"message": []},
        )

        # Update the chat object with the new message
        chat_message = data

        if isinstance(chat.message, list):
            chat.message.append(chat_message)
        else:
            chat.message = [chat_message]

        chat.save()
        return Response(
                status=status.HTTP_200_OK,
                data={
                    KEY_MESSAGE: "category data sent successfully.",
                    KEY_PAYLOAD: "on working", #MasterCategorySerializer(category, many = True, context=context).data,
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
		    chat = BlackhallChat.objects.get(user=user, timestamp__date=today)
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
		        "data": chat.message  # Returning the list of messages
		    },
		)