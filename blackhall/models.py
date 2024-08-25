from django.db import models
from user.models import User
import uuid
from content.models import Content

class BlackhallChat(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	message = models.JSONField(null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
	    return f"{self.user}"