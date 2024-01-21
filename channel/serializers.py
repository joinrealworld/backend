from channel.models import *
from rest_framework import serializers
from rest_framework.response import Response
from django.urls import reverse
from django.conf import settings
import string
import random

class CategorySerializer(serializers.ModelSerializer):
	# category_pic = serializers.SerializerMethodField()
	no_of_courses = serializers.SerializerMethodField()
	completed = serializers.SerializerMethodField()
    
	class Meta:
		model = Category
		fields = ('id', 'name', 'category_pic', 'description', 'no_of_courses', 'completed')

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
		return str(random.randrange(0, 100))

class CoursesSerializer(serializers.ModelSerializer):
	description = serializers.SerializerMethodField()
	completed = serializers.SerializerMethodField()
	course_pic = serializers.SerializerMethodField()
	is_favorite = serializers.SerializerMethodField()

	class Meta:
		model = Courses
		fields = ('id', 'name', 'description', 'completed', 'is_favorite', 'course_pic',)

	def get_description(self, obj):
		return "This is course description"

	def get_completed(self, obj):
		return str(random.randrange(0, 100))

	def get_course_pic(self, obj):
		return "media/course_pic/1/crypto-crash.jpeg"

	def get_is_favorite(self, obj):
		return False

class CoursesDataSerializer(serializers.ModelSerializer):
	description = serializers.SerializerMethodField()
	completed = serializers.SerializerMethodField()
	is_favorite = serializers.SerializerMethodField()
	course_pic = serializers.SerializerMethodField()

	class Meta:
		model = Courses
		fields = ('id', 'name', 'description', 'completed', 'course_pic', 'is_favorite', 'data')

	def get_description(self, obj):
		return "This is course description"

	def get_completed(self, obj):
		return str(random.randrange(0, 100))

	def get_course_pic(self, obj):
		return "media/course_pic/1/crypto-crash.jpeg"

	def get_is_favorite(self, obj):
		return False

class CourseQuizDataSerializer(serializers.ModelSerializer):

	class Meta:
		model = CourseQuiz
		fields = ('id', 'course', 'index', 'data')