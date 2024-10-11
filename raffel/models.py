from django.db import models
import uuid
from user.models import User
# Create your models here.
class Raffel(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	index = models.PositiveIntegerField(default=1, blank=False, null=False)
	timestamp = models.DateTimeField(auto_now_add=True)

	class Meta:
	    ordering = ['-timestamp']
	    indexes = [
	        models.Index(fields=['timestamp']),
	        models.Index(fields=['user']),
	    ]

