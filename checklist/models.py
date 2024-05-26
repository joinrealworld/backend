from django.db import models
import string
import uuid
from user.models import User
from django.utils import timezone


# Create your models here.
class MasterCheckList(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	checklist = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	copied_at = models.DateTimeField(default=timezone.now)

	def save(self, *args, **kwargs):
	    if not self.copied_at:
	        self.copied_at = timezone.now()  # Automatically set copied_at if not provided
	    super().save(*args, **kwargs)

class UserDailyCheckList(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	master_checklist = models.ForeignKey(MasterCheckList, on_delete=models.CASCADE, null=False, blank = False)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
	    return f"{self.id}"

class DailyChecked(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank = False)
	checklist = models.ForeignKey(UserDailyCheckList, on_delete=models.CASCADE, null=True, blank = True)
	selected = models.CharField(max_length=20, null=True, blank = True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
	    return f"{self.id}"