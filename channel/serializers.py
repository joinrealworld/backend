from channel.models import *
from rest_framework import serializers
from rest_framework.response import Response
from django.urls import reverse
from django.conf import settings
import string
import random
from user.models import User
from channel.scripts import count_completed_category, count_completed_course

class MasterCategorySerializer(serializers.ModelSerializer):
	# category_pic = serializers.SerializerMethodField()
	no_of_category = serializers.SerializerMethodField()
	online_users = serializers.SerializerMethodField()
    
	class Meta:
		model = MasterCategory
		fields = ('id', 'uuid','name', 'category_pic', 'category_pic2','description', 'no_of_category', 'online_users')

	# def get_category_pic(self, obj):
		# # request = self.context.get('request')

		# # # Check if request is available
		# # if request:
		# # 	# Generate absolute URL using reverse and request
		# # 	absolute_url = request.build_absolute_uri(obj.category_pic.url)
		# # 	return absolute_url

		# # Fallback to relative URL if request is not available
		# return obj.category_pic if obj.category_pic else ""

	def get_no_of_category(self, obj):
		return Category.objects.filter(master_category = obj).count()

	def get_online_users(self, obj):
		return User.objects.filter(is_online = True).count()


class CategorySerializer(serializers.ModelSerializer):
	# category_pic = serializers.SerializerMethodField()
	no_of_courses = serializers.SerializerMethodField()
	completed = serializers.SerializerMethodField()
	master_category__uuid = serializers.SerializerMethodField()
    
	class Meta:
		model = Category
		fields = ('id', 'uuid','name', 'category_pic', 'description', 'no_of_courses', 'completed', 'master_category__uuid')

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

	def get_master_category__uuid(self, obj):
		return obj.master_category.uuid if obj.master_category else None

class CoursesSerializer(serializers.ModelSerializer):
	completed = serializers.SerializerMethodField()
	is_favorite = serializers.SerializerMethodField()
	lessons = serializers.SerializerMethodField()
	category_uuid = serializers.SerializerMethodField()
	last_saved = serializers.SerializerMethodField()

	class Meta:
		model = Courses
		fields = ('id', 'uuid','name', 'completed', 'is_favorite', 'pic', 'category_uuid', 'last_saved','lessons')

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

	def get_category_uuid(self, obj):
		return obj.category.uuid

	def get_last_saved(self, obj):
		user_id = self.context.get('user_id')
		last_saved = LastCourseContent.objects.filter(user = User.objects.get(pk=user_id), course__uuid = obj.uuid)
		if last_saved:
			return last_saved.last().content_uuid
		else:
			None


class CoursesDataSerializer(serializers.ModelSerializer):
	completed = serializers.SerializerMethodField()
	is_favorite = serializers.SerializerMethodField()
	data = serializers.SerializerMethodField()
	last_checked = serializers.SerializerMethodField()
	last_saved = serializers.SerializerMethodField()

	class Meta:
		model = Courses
		fields = ('id', 'uuid', 'name', 'description', 'completed', 'pic', 'is_favorite', 'last_checked', 'last_saved','data')

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

	def get_last_saved(self, obj):
		user_id = self.context.get('user_id')
		last_saved = LastCourseContent.objects.filter(user = User.objects.get(pk=user_id), course__uuid = obj.uuid)
		if last_saved:
			return last_saved.last().content_uuid
		else:
			None


class CourseQuizDataSerializer(serializers.ModelSerializer):

	class Meta:
		model = CourseQuiz
		fields = ('id', 'uuid', 'course', 'index', 'data')



class LastCourseContentSerializer(serializers.ModelSerializer):
    course = serializers.SlugRelatedField(slug_field='uuid', queryset=Courses.objects.all())
    content_uuid = serializers.CharField()

    class Meta:
        model = LastCourseContent
        fields = ['uuid', 'content_uuid', 'course', 'user']
        read_only_fields = ['user']

    def validate(self, data):
        # Ensure the provided course UUID exists
        course_uuid = data.get('course')
        print("162-----", course_uuid)
        try:
            course = Courses.objects.get(uuid=course_uuid)
            print("164----", course)
            data['course'] = course
        except Courses.DoesNotExist:
            raise serializers.ValidationError({"course": "Course with this UUID does not exist."})

        return data

    def create(self, validated_data):
        course = validated_data.get('course')
        print("171----", self.context['request'].user)
        user = self.context['request'].user

        # Delete any existing LastCourseContent object with the same course and user
        LastCourseContent.objects.filter(course=course, user=user).delete()

        # Create and return the new LastCourseContent object
        return LastCourseContent.objects.create(**validated_data)


