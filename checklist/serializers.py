from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from checklist.models import *


# class MasterPollOptionSerializer(serializers.ModelSerializer):
# 	no_of_selected_by_user = serializers.SerializerMethodField()

# 	class Meta:
# 		model = MasterPollOption
# 		fields = ( 'id','uuid', 'option', 'no_of_selected_by_user')

# 	def get_no_of_selected_by_user(self, obj):
# 		user_count = User.objects.all().count()
# 		user_poll_count = UserPoll.objects.filter(is_checked = True, selected_option = obj).count()
# 		return str(user_poll_count) + " out of " + str(user_count)

