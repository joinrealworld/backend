from django.db import models
from user.models import User
import uuid

# Create your models here.
class CustomerDetails(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
	customer_id = models.CharField(max_length=128,null=True, blank=True)
	data = models.JSONField(null=True, blank=True)
	has_card = models.BooleanField(default = False)
	
	def __str__(self):
		return f"{self.id} -- {self.user}"