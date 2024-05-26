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
from constants.response import KEY_MESSAGE, KEY_PAYLOAD, KEY_STATUS
from constants.commons import handle_exceptions
from user.permissions import IsUserAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from user.serializers import UserSimpleSerializer
from user.models import User

class FetchMasterCategoryAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def get(self, request):
        category = MasterCategory.objects.all().order_by('id')
        context = {"user_id":request.user.id, 'request': self.request}
        return Response(
                status=status.HTTP_200_OK,
                data={
                    KEY_MESSAGE: "category data sent successfully.",
                    KEY_PAYLOAD: MasterCategorySerializer(category, many = True, context=context).data,
                    KEY_STATUS: 1
                },
            )

class FetchCategoryAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def get(self, request, master_category_id):
        category = Category.objects.filter(master_category__uuid = master_category_id)
        context = {"user_id":request.user.id, 'request': self.request}
        return Response(
                status=status.HTTP_200_OK,
                data={
                    KEY_MESSAGE: "category data sent successfully.",
                    KEY_PAYLOAD: CategorySerializer(category, many = True, context=context).data,
                    KEY_STATUS: 1
                },
            )

class FetchCourseCategoryAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def get(self, request, category_id):
        courses = Courses.objects.filter(category__uuid = category_id)
        context = {"user_id":request.user.id}
        return Response(
                status=status.HTTP_200_OK,
                data={
                    KEY_MESSAGE: "courses sent successfully.",
                    KEY_PAYLOAD: CoursesSerializer(courses, many = True, context=context).data,
                    KEY_STATUS: 1
                },
            )

class FetchCourseDataAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def get(self, request, course_id):
        courses = Courses.objects.filter(uuid = course_id)
        context = {"user_id":request.user.id, "course_id": courses.last().uuid}
        return Response(
                status=status.HTTP_200_OK,
                data={
                    KEY_MESSAGE: "course data sent successfully.",
                    KEY_PAYLOAD: CoursesDataSerializer(courses.last(), context = context).data,
                    KEY_STATUS: 1
                },
            )

class FetchCourseQuizAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def get(self, request, course_id, quiz_index):
    	course_quiz = CourseQuiz.objects.get(course__uuid = course_id, index = quiz_index)
    	return Response(
                status=status.HTTP_200_OK,
                data={
                    KEY_MESSAGE: "course data sent successfully.",
                    KEY_PAYLOAD: CourseQuizDataSerializer(course_quiz).data,
                    KEY_STATUS: 1
                },
            )

class AddFavouriteContentAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def post(self, request):
        course_id = request.data.get("course_id")
        content_uuid = request.data.get("content_uuid")
        course = Courses.objects.get(uuid=course_id)
        favorite_content, created = FavoriteCourseContent.objects.get_or_create(content_uuid=content_uuid, course=course, user=request.user)

        if not created:
            # If FavoriteCourseContent already exists, remove it
            favorite_content.delete()
            message = "Content removed from favorites."
        else:
            message = "Content added to favorites."

        return Response(
            {
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: message,
                KEY_STATUS: 1
            },
            status=status.HTTP_200_OK
        )

class AddFavouriteCourseAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def post(self, request):
        course_id = request.data.get("course_id")
        course = Courses.objects.get(uuid=course_id)
        favorite_course, created = FavoriteCourse.objects.get_or_create(course=course, user=request.user)
        if not created:
            favorite_course.delete()  # Delete the existing FavoriteCourse object
            message = "Course removed from favorites."
        else:
            message = "Course added to favorites."
        return Response(
            {
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: message,
                KEY_STATUS: 1
            },
            status=status.HTTP_200_OK
        )

class MarkCompleteContentAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
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
                    KEY_PAYLOAD: "Section Marked Completed.",
                    KEY_STATUS: 1
                },
            )

class FetchFavouriteCoursesAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def get(self, request):
        user = request.user
        context = {"user_id": request.user.id, 'request': self.request}

        # Fetch favorite courses with related courses and categories prefetched
        favorite_courses = FavoriteCourse.objects.filter(user=user).select_related('course__category')

        # Create a dictionary to store favorite courses grouped by category
        favorite_courses_by_category = {}

        # Group favorite courses by category
        for favorite_course in favorite_courses:
            category_name = favorite_course.course.category.name
            category_obj = favorite_course.course.category
            if category_name not in favorite_courses_by_category:
                favorite_courses_by_category[category_name] = {"category": category_obj, "courses": []}
            favorite_courses_by_category[category_name]["courses"].append(favorite_course.course)

        # Serialize the data
        serialized_data = []
        for category_name, data in favorite_courses_by_category.items():
            serialized_category = CategorySerializer(data["category"], context=context).data
            serialized_courses = CoursesSerializer(data["courses"], context=context, many=True).data
            serialized_data.append({
                "category": serialized_category,
                "courses": serialized_courses
            })

        return Response(
            {
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: serialized_data,
                KEY_STATUS: 1
            },
            status=status.HTTP_200_OK
        )

class FetchInProgressCoursesAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def get(self, request):
        user = request.user
        context = {"user_id": request.user.id, 'request': self.request}
        categories = Category.objects.all()
        in_progress_categories = [category for category in categories if count_completed_category(user, category) not in [0, 0.00, 100.0, 100, 100.00]]
        in_progress_courses = [course for category in in_progress_categories for course in Courses.objects.filter(category=category) if count_completed_course(user, course) not in [0, 0.00, 100.0, 100, 100.00]]
        serialized_data = CoursesSerializer(in_progress_courses, context=context, many=True).data
        return Response(
            {
                KEY_MESSAGE: "Success",
                KEY_PAYLOAD: serialized_data,
                KEY_STATUS: 1
            },
            status=status.HTTP_200_OK
        )


class FetchCategoryUsersAPIView(APIView):
    permission_classes = [IsUserAuthenticated]

    @handle_exceptions
    def get(self, request, master_category_id):
        category = Category.objects.filter(master_category__uuid = master_category_id)
        context = {"user_id":request.user.id, 'request': self.request}
        user = User.objects.all()
        return Response(
                status=status.HTTP_200_OK,
                data={
                    KEY_MESSAGE: "category data sent successfully.",
                    KEY_PAYLOAD: UserSimpleSerializer(user, many = True, context=context).data,
                    KEY_STATUS: 1
                },
            )
