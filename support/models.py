from django.db import models

# Create your models here.
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

class Support(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
	messages = models.JSONField(null=True, blank=True, default=list)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
	    return f"Support Chat of {self.user}"

	class Meta:
	    constraints = [
	        models.UniqueConstraint(fields=['user'], name='unique_support_user')
	    ]