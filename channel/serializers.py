from channel.models import *
from rest_framework import serializers
from rest_framework.response import Response
from django.urls import reverse
from django.conf import settings
import string
import random
from user.models import User
from channel.scripts import count_completed_category, count_completed_course

class CategorySerializer(serializers.ModelSerializer):
	# category_pic = serializers.SerializerMethodField()
	no_of_courses = serializers.SerializerMethodField()
	completed = serializers.SerializerMethodField()
    
	class Meta:
		model = Category
		fields = ('id', 'uuid','name', 'category_pic', 'description', 'no_of_courses', 'completed')

	# def get_category_pic(self, obj):
		# # request = self.context.get('request')

		# # # Check if request is available
		# # if request:
		# # 	# Generate absolute URL using reverse and request
		# # 	absolute_url = request.build_absolute_uri(obj.category_pic.url)
		# # 	return absolute_url

		# # Fallback to relative URL if request is not available
		# return obj.category_pic if obj.category_pic else ""

	def get_no_of_courses(self, obj):
		return Courses.objects.filter(category = obj).count()

	def get_completed(self, obj):
		user_id = self.context.get('user_id')
		user = User.objects.get(pk=user_id)
		return count_completed_category(user, obj)

class CoursesSerializer(serializers.ModelSerializer):
	completed = serializers.SerializerMethodField()
	is_favorite = serializers.SerializerMethodField()
	lessons = serializers.SerializerMethodField()

	class Meta:
		model = Courses
		fields = ('id', 'uuid','name', 'completed', 'is_favorite', 'pic', 'lessons')

	def get_completed(self, obj):
		user_id = self.context.get('user_id')
		user = User.objects.get(pk=user_id)
		return count_completed_course(user, obj)

	def get_is_favorite(self, obj):
		user_id = self.context.get('user_id')
		favourite = FavoriteCourse.objects.filter(user = User.objects.get(pk=user_id), course = obj)
		if favourite.exists():
			return True
		return False

	def get_lessons(self, obj):
		return len(obj.data)

class CoursesDataSerializer(serializers.ModelSerializer):
	completed = serializers.SerializerMethodField()
	is_favorite = serializers.SerializerMethodField()
	data = serializers.SerializerMethodField()
	last_checked = serializers.SerializerMethodField()

	class Meta:
		model = Courses
		fields = ('id', 'uuid', 'name', 'description', 'completed', 'pic', 'is_favorite', 'last_checked','data')

	def get_completed(self, obj):
		user_id = self.context.get('user_id')
		user = User.objects.get(pk=user_id)
		return count_completed_course(user, obj)

	def get_is_favorite(self, obj):
		user_id = self.context.get('user_id')
		favourite = FavoriteCourse.objects.filter(user = User.objects.get(pk=user_id), course = obj)
		if favourite.exists():
			return True
		return False

	def get_last_checked(self, obj):
		user_id = self.context.get('user_id')
		course_id = self.context.get('course_id')
		completed_content = CompleteContent.objects.filter(user__id = user_id, course__uuid = course_id)
		if completed_content.exists():
			return completed_content.last().content_uuid
		return None

	def fomat_data(self, data, obj):
		user_id = self.context.get('user_id')
		user = User.objects.get(pk=user_id)
		formated_data = []
		for data_obj in data:
			uuid = data_obj['uuid']
			favourite = FavoriteCourseContent.objects.filter(content_uuid = uuid, user = user, course = obj)
			if favourite.exists():
				data_obj["is_favourite"] = True
			formated_data.append(data_obj)
		return formated_data

	def get_data(self, obj):
		return self.fomat_data(obj.data, obj)

class CourseQuizDataSerializer(serializers.ModelSerializer):

	class Meta:
		model = CourseQuiz
		fields = ('id', 'uuid', 'course', 'index', 'data')