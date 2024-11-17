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
from django.core.validators import MinValueValidator

# Create your models here.
class QuizScore(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
	score = models.FloatField(validators=[MinValueValidator(0.0)], null=True, blank=True)
	failer_count = models.PositiveIntegerField(default=0, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']


	def __str__(self):
		return f"{self.uuid}"

