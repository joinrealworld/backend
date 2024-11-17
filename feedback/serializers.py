from rest_framework import serializers
from feedback.models import Feedback
from user.serializers import UserSimpleSerializer
from channel.serializers import *

class FeedbackSerializer(serializers.ModelSerializer):
	user = serializers.SerializerMethodField()
	category = serializers.SerializerMethodField()
	master_category = serializers.SerializerMethodField()
	course = serializers.SerializerMethodField()


	class Meta:
	    model = Feedback
	    fields = ['uuid', 'course','content', 'category', 'master_category','user', 'description', 'created_at']
	    read_only_fields = ['uuid', 'user', 'created_at']  # Prevent users from modifying these fields

	def get_user(self, instance):
	    return UserSimpleSerializer(instance.user).data

	def get_course(self, obj):
		context = {"user_id":obj.user.id}
		return CoursesSerializer(obj.course, context=context).data

	def get_category(self, obj):
		context = {"user_id":obj.user.id}
		return CategorySerializer(obj.course.category, context=context).data

	def get_master_category(self, obj):
		return MasterCategorySerializer(obj.course.category.master_category).data

class SendFeedbackSerializer(serializers.Serializer):
    content = serializers.DictField(required=True)
    master_category = serializers.UUIDField(required=True)
    category = serializers.UUIDField(required=True)
    course = serializers.UUIDField(required=True)
    description = serializers.CharField(required=True)