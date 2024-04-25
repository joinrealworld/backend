from django.db import models
from user.models import *

# Create your models here.
class MasterPollQuetion(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	quetion = models.CharField(max_length=255, blank=False, null=False, )
	created_at = models.DateTimeField(auto_now_add=True)

class MasterPollOption(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	option = models.CharField(max_length=255, blank=False, null=False, )
	poll_quetion = models.ForeignKey(MasterPollQuetion, on_delete=models.CASCADE, null=False, blank = False)
	created_at = models.DateTimeField(auto_now_add=True)

class UserPoll(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	selected_option = models.ForeignKey(MasterPollOption, on_delete=models.CASCADE, null=True, blank = True)
	is_checked = models.BooleanField(default=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank = False)
	poll_quetion = models.ForeignKey(MasterPollQuetion, on_delete=models.CASCADE, null=True, blank = True)
	created_at = models.DateTimeField(auto_now_add=True)

class MasterCheckList(models.Model):
	checklist_data = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

class UserCheckedList(models.Model):
	checked_data = models.TextField()
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank = False)
	created_at = models.DateTimeField(auto_now_add=True)
