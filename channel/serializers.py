from channel.models import *
from rest_framework import serializers
from rest_framework.response import Response
from django.urls import reverse
from django.conf import settings
import string
import random

class CategorySerializer(serializers.ModelSerializer):
	category_pic = serializers.SerializerMethodField()
	no_of_courses = serializers.SerializerMethodField()
    
	class Meta:
		model = Category
		fields = ('id', 'name', 'category_pic', 'description', 'no_of_courses')

	def get_category_pic(self, obj):
		request = self.context.get('request')

		# Check if request is available
		if request:
			# Generate absolute URL using reverse and request
			absolute_url = request.build_absolute_uri(obj.category_pic.url)
			return absolute_url

		# Fallback to relative URL if request is not available
		return obj.category_pic.url if obj.category_pic else ""

	def get_no_of_courses(self, obj):
		return Courses.objects.filter(category = obj).count()

class CoursesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Courses
		fields = ('id', 'name')

class CoursesDataSerializer(serializers.ModelSerializer):

	class Meta:
		model = Courses
		fields = ('id', 'name', 'data')

class CourseQuizDataSerializer(serializers.ModelSerializer):

	class Meta:
		model = CourseQuiz
		fields = ('id', 'course', 'index', 'data')