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
from channel.models import *
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
from channel.scripts import *
from constants.response import KEY_MESSAGE, KEY_PAYLOAD
from user.permissions import IsUserAuthenticated

class FetchCategoryAPIView(APIView):
	permission_classes = [IsUserAuthenticated]

	def get(self, request):
		category = Category.objects.all()
		return Response(
                status=status.HTTP_200_OK,
                data={
                    KEY_MESSAGE: "category data sent successfully.",
                    KEY_PAYLOAD: CategorySerializer(category, many = True, context={'request': self.request}).data
                },
            )

class FetchCourseCategoryAPIView(APIView):
	permission_classes = [IsUserAuthenticated]

	def get(self, request, category_id):
		courses = Courses.objects.filter(category__uuid = category_id) | Courses.objects.filter(category__pk = category_id)
		return Response(
                status=status.HTTP_200_OK,
                data={
                    KEY_MESSAGE: "courses sent successfully.",
                    KEY_PAYLOAD: CoursesSerializer(courses, many = True).data
                },
            )

class FetchCourseDataAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    def get(self, request, course_id):
        courses = Courses.objects.filter(pk = course_id)
        print("65-----", courses)
        return Response(
                status=status.HTTP_200_OK,
                data={
                    KEY_MESSAGE: "course data sent successfully.",
                    KEY_PAYLOAD: CoursesDataSerializer(courses.last()).data
                },
            )

class FetchCourseQuizAPIView(APIView):
	permission_classes = [IsUserAuthenticated]

	def get(self, request, course_id, quiz_index):
		course_quiz = CourseQuiz.objects.get(course__id = course_id, index = quiz_index) | CourseQuiz.objects.get(course__uuid = course_id, index = quiz_index)
		return Response(
                status=status.HTTP_200_OK,
                data={
                    KEY_MESSAGE: "course data sent successfully.",
                    KEY_PAYLOAD: CourseQuizDataSerializer(course_quiz).data
                },
            )

class AddFavouriteAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    def post(self, request):
        course_id = request.data.get("course_id")
        content_uuid = request.data.get("content_uuid")
        course = Courses.objects.get(uuid=course_id)
        course_data = course.data
        for data in course_data:
            if data['uuid'] == content_uuid:
                print("97-----", data)
        return Response(
                status=status.HTTP_200_OK,
                data={
                    KEY_MESSAGE: "Success",
                    KEY_PAYLOAD: "Content Added to Favourite."
                },
            )

