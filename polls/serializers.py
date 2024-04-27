from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from polls.models import *

class OptionSerializer(serializers.Serializer):
	options = serializers.CharField()

class CreatePollSerializer(serializers.Serializer):
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
		user_poll_count = UserPoll.objects.filter(is_checked = True, selected_option = obj).count()
		return str(user_poll_count) + " out of " + str(user_count)

class MasterPollQuetionSerializer(serializers.ModelSerializer):
	options = MasterPollOptionSerializer(source='masterpolloption_set', many=True)

	class Meta:
		model = MasterPollQuetion
		fields = ('id', 'uuid','quetion', 'options', 'created_at')

class AnswerPollSerializer(serializers.Serializer):
	question_id = serializers.CharField()
	selected_option_id = serializers.CharField()