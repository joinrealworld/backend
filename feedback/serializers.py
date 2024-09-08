from rest_framework import serializers
from feedback.models import Feedback
from user.serializers import UserSimpleSerializer

class FeedbackSerializer(serializers.ModelSerializer):
	user = serializers.SerializerMethodField()

	class Meta:
	    model = Feedback
	    fields = ['uuid', 'content_uuid', 'user', 'description', 'created_at']
	    read_only_fields = ['uuid', 'user', 'created_at']  # Prevent users from modifying these fields

	def get_user(self, instance):
	    return UserSimpleSerializer(instance.user).data
