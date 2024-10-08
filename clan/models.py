from django.db import models
from user.models import User
import uuid 

# Create your models here.
class Clan(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)

	class Meta:
	    ordering = ['-timestamp']
	    indexes = [
	        models.Index(fields=['timestamp']),
	        models.Index(fields=['user']),
	    ]

