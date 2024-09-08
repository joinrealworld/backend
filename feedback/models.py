import pytz
import random
from datetime import datetime, timedelta
from django.conf import settings
from django.core.validators import ValidationError
from django.db import models
from math import sin, cos, sqrt, atan2, radians
from ckeditor.fields import RichTextField
import string
import uuid
from user.models import User

# Create your models here.
class Feedback(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	content_uuid = models.CharField(max_length=128,null=True, blank=True)
	user = models.ForeignKey(User, related_name='user_feedback',null=False, blank=False, on_delete=models.CASCADE)
	description = RichTextField(blank = True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']


	def __str__(self):
		return f"{self.uuid}"
