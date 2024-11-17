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
from feedback.models import *
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
from feedback.serializers import *
from channel.models import *

class SendFeedbackAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    # @handle_exceptions
    def post(self, request):
        serializer = SendFeedbackSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                KEY_MESSAGE: "Invalid feedback data.",
                KEY_PAYLOAD: serializer.errors,
                KEY_STATUS: 0
                },
            )

        validated_data = serializer.validated_data
        user = request.user
        course_uuid = validated_data["course"]
        category_uuid = validated_data["category"]
        master_category_uuid = validated_data["master_category"]
        course = Courses.objects.get(uuid = course_uuid)
        category = Category.objects.get(uuid = category_uuid)
        master_category = MasterCategory.objects.get(uuid = master_category_uuid)

        # Create Feedback instance and save
        feedback = Feedback.objects.create(
            content = validated_data["content"],
            course = course,
            category=category,
            master_category = master_category,
            user=user,
            description=validated_data["description"]
        )

        return Response(
            status=status.HTTP_201_CREATED,
            data={
                KEY_MESSAGE: "Feedback sent successfully.",
                KEY_PAYLOAD: FeedbackSerializer(feedback).data,
                KEY_STATUS: 1,
            },
        )


class FetchFeedbackAPIView(APIView):
    permission_classes = [IsLoggedInUserOrAdmin]

    @handle_exceptions
    def get(self, request):
        user = request.user

        # Fetch all feedback for the current user
        feedback_list = Feedback.objects.all().order_by("created_at")

        if not feedback_list.exists():
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    KEY_MESSAGE: "No feedback found for the user.",
                    KEY_STATUS: 0,
                },
            )

        
        return Response(
            status=status.HTTP_200_OK,
            data={
                KEY_MESSAGE: "Feedback retrieved successfully.",
                KEY_PAYLOAD: FeedbackSerializer(feedback_list, many=True).data,
                KEY_STATUS: 1,
            },
        )