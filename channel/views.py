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
from django.core.exceptions import ObjectDoesNotExist


class FetchCategoryAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    def get(self, request):
        category = Category.objects.all()
        context = {"user_id":request.user.id, 'request': self.request}
        return Response(
                status=status.HTTP_200_OK,
                data={
                    KEY_MESSAGE: "category data sent successfully.",
                    KEY_PAYLOAD: CategorySerializer(category, many = True, context=context).data
                },
            )

class FetchCourseCategoryAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    def get(self, request, category_id):
        courses = Courses.objects.filter(category__uuid = category_id) | Courses.objects.filter(category__pk = category_id)
        context = {"user_id":request.user.id}
        return Response(
                status=status.HTTP_200_OK,
                data={
                    KEY_MESSAGE: "courses sent successfully.",
                    KEY_PAYLOAD: CoursesSerializer(courses, many = True, context=context).data
                },
            )

class FetchCourseDataAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    def get(self, request, course_id):
        courses = Courses.objects.filter(pk = course_id)
        context = {"user_id":request.user.id}
        return Response(
                status=status.HTTP_200_OK,
                data={
                    KEY_MESSAGE: "course data sent successfully.",
                    KEY_PAYLOAD: CoursesDataSerializer(courses.last(), context = context).data
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

class AddFavouriteContentAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    def post(self, request):
        course_id = request.data.get("course_id")
        content_uuid = request.data.get("content_uuid")
        course = Courses.objects.get(uuid=course_id)
        course_data = course.data
        for data in course_data:
            if data['uuid'] == content_uuid:
                FavoriteCourseContent.objects.get_or_create(content_uuid=content_uuid, course = course, user = request.user)
                return Response(
                        status=status.HTTP_200_OK,
                        data={
                            KEY_MESSAGE: "Success",
                            KEY_PAYLOAD: "Content Added to Favourite."
                        },
                    )
        return Response(
                        status=status.HTTP_200_OK,
                        data={
                            KEY_MESSAGE: "Error",
                            KEY_PAYLOAD: "Not found any content matched with course id and content id."
                        },
                    )

class RemoveFavouriteContentAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    def post(self, request):
        course_id = request.data.get("course_id")
        content_uuid = request.data.get("content_uuid")
        course = Courses.objects.get(uuid=course_id)
        course_data = course.data
        try:
            existing_instance = FavoriteCourseContent.objects.get(content_uuid=content_uuid, course=course, user=request.user)
            existing_instance.delete()
        except ObjectDoesNotExist:
            pass
        return Response(
                status=status.HTTP_200_OK,
                data={
                    KEY_MESSAGE: "Success",
                    KEY_PAYLOAD: "Content Removed from Favourite."
                },
            )


class AddFavouriteCourseAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    def post(self, request):
        course_id = request.data.get("course_id")
        course = Courses.objects.get(uuid=course_id)
        FavoriteCourse.objects.get_or_create(course = course, user = request.user)
        return Response(
                status=status.HTTP_200_OK,
                data={
                    KEY_MESSAGE: "Success",
                    KEY_PAYLOAD: "Course Added to Favourite."
                },
            )
        

class RemoveFavouriteCourseAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    def post(self, request):
        course_id = request.data.get("course_id")
        course = Courses.objects.get(uuid=course_id)
        try:
            existing_instance = FavoriteCourse.objects.get(course=course, user=request.user)
            existing_instance.delete()
        except ObjectDoesNotExist:
            pass
        return Response(
                status=status.HTTP_200_OK,
                data={
                    KEY_MESSAGE: "Success",
                    KEY_PAYLOAD: "Course Removed from Favourite."
                },
            )

class MarkCompleteContentAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    def post(self, request):
        course_id = request.data.get("course_id")
        content_id = request.data.get("content_id")
        user = request.user
        course = Courses.objects.get(uuid=course_id)
        CompleteContent.objects.get_or_create(course = course, user=user, content_uuid=content_id)
        return Response(
                status=status.HTTP_200_OK,
                data={
                    KEY_MESSAGE: "Success",
                    KEY_PAYLOAD: "Section Marked Completed."
                },
            )


