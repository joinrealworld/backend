from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from checklist.models import *


class MasterCheckListSerializer(serializers.ModelSerializer):
	checklist_data = serializers.SerializerMethodField()

	class Meta:
		model = MasterCheckList
		fields = ( 'checklist_data',)

	def get_checklist_data(self, obj):
		return obj.data.split(",")

class UserDailyCheckListSerializer(serializers.ModelSerializer):
	selected_data = serializers.SerializerMethodField()
	user = serializers.SerializerMethodField()

	class Meta:
		model = UserDailyCheckList
		fields = ( 'user', 'selected_data', 'created_at')

	def get_selected_data(self, obj):
		return obj.selected.split(",")

	def get_user(self, obj):
		return obj.user.username