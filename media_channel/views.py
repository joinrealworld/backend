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
from media_channel.serializers import *
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404


class SendMessageAPIView(APIView):
    permission_classes = [IsLoggedInUser]

    def post(self, request):
        serializer = MediaChannelSerializer(data=request.data, context={'request': request})
        user = request.user
        if user.coin < 200:
             return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    "message": "User Does not have enough coin to send Message.",
                    "status": 0
                },
            )

        user.coin = user.coin-200
        user.save()
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Message sent successfully.",
                    "status": 1,
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    "message": "Failed to send message.",
                    "status": 0,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class MediaChannelPagination(PageNumberPagination):
    page_size = 10  # Number of messages per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class FetchMessagesAPIView(APIView):
    permission_classes = [IsLoggedInUser]

    def get(self, request):
        paginator = MediaChannelPagination()
        messages = MediaChannel.objects.all().order_by('timestamp')
        result_page = paginator.paginate_queryset(messages, request)
        serializer = MediaChannelDataSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)



class LikeMessagesAPIView(APIView):
    permission_classes = [IsLoggedInUser]

    def post(self, request):
        user = request.user
        message_uuid = request.data.get("message_uuid")

        if not message_uuid:
            return Response(
                {
                    "message": "Message UUID is required.",
                    "status": 0,
                    "errors": {"message_uuid": ["This field is required."]}
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get the MediaChannel message object or return 404 if not found
        media_channel = get_object_or_404(MediaChannel, uuid=message_uuid)

        # Check if the user has already liked this message
        if MediaChannelLike.objects.filter(media_channel=media_channel, user=user).exists():
            return Response(
                {
                    "message": "You have already liked this message.",
                    "status": 0,
                    "data": "Already liked."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create a new like
        MediaChannelLike.objects.create(media_channel=media_channel, user=user)

        return Response(
            {
                "message": "Message liked successfully.",
                "status": 1,
                "data": "Message liked successfully."
            },
            status=status.HTTP_201_CREATED
        )
