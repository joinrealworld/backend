from rest_framework import serializers
from support.models import Support
from user.serializers import UserSimpleSerializer


class SupportSerializer(serializers.ModelSerializer):
	user = serializers.SerializerMethodField()

	class Meta:
	    model = Support
	    fields = ['uuid', 'user','messages', 'created_at']

	def get_user(self, instance):
	    return UserSimpleSerializer(instance.user).data

class SupportUserListSerializer(serializers.ModelSerializer):
	user = serializers.SerializerMethodField()

	class Meta:
	    model = Support
	    fields = ['uuid', 'user', 'created_at']

	def get_user(self, instance):
	    return UserSimpleSerializer(instance.user).data
