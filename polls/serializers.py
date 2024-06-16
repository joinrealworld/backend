from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from polls.models import *
from user.serializers import UserSimpleSerializer

class OptionSerializer(serializers.Serializer):
	options = serializers.CharField()

class CreatePollSerializer(serializers.Serializer):
	master_category = serializers.UUIDField()
	question = serializers.CharField()
	options = serializers.ListField(child=serializers.CharField())

	def validate_options(self, value):
	    if len(value) < 2:
	        raise serializers.ValidationError("At least two options are required.")
	    return value

class MasterPollOptionSerializer(serializers.ModelSerializer):
	no_of_selected_by_user = serializers.SerializerMethodField()

	class Meta:
		model = MasterPollOption
		fields = ( 'id','uuid', 'option', 'no_of_selected_by_user')

	def get_no_of_selected_by_user(self, obj):
		user_count = User.objects.all().count()
		return UserPoll.objects.filter(is_checked = True, selected_option = obj).count()

class MasterPollQuetionSerializer(serializers.ModelSerializer):
	options = MasterPollOptionSerializer(source='masterpolloption_set', many=True)
	admin_data = serializers.SerializerMethodField()

	class Meta:
		model = MasterPollQuetion
		fields = ('id', 'uuid','quetion', 'options', 'admin_data','created_at')

	def get_admin_data(self, obj):
		admin_users = User.objects.filter(is_admin=True)
		return UserSimpleSerializer(admin_users, many=True).data

class AnswerPollSerializer(serializers.Serializer):
	question_id = serializers.CharField()
	selected_option_id = serializers.CharField()