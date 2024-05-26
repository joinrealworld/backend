from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from checklist.models import *


class MasterCheckListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterCheckList
        fields = ('checklist',)

class DailyCheckedSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = DailyChecked
        fields = ('user', 'selected', 'created_at')

    def get_user(self, instance):
        return instance.user.username

class UserDailyCheckListSerializer(serializers.ModelSerializer):
    checked = serializers.SerializerMethodField()
    checklist = serializers.SerializerMethodField()

    class Meta:
        model = UserDailyCheckList
        fields = ('uuid', 'checklist', 'checked')

    def get_checklist(self, instance):
    	return instance.master_checklist.checklist

    def get_checked(self, instance):
        checked_objects = instance.dailychecked_set.all()
        grouped_checked = {}

        for checked in checked_objects:
            selected_key = checked.selected
            if selected_key not in grouped_checked:
                grouped_checked[selected_key] = []
            grouped_checked[selected_key].append(DailyCheckedSerializer(checked).data)

        return grouped_checked

