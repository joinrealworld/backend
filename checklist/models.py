from django.db import models
import string
import uuid
from user.models import User

# Create your models here.
class MasterCheckList(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	data = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
	    return f"{self.id}"

class UserDailyCheckList(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	selected = models.TextField()
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank = False)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
	    return f"{self.id}"