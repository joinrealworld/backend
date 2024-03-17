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
	created_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return f"{self.id} -- {self.user} -- {self.created_at}"

class CustomerPayment(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
	price_id = models.CharField(max_length=128,null=True, blank=True)
	customer_id = models.CharField(max_length=128,null=True, blank=True)
	subscription_id = models.CharField(max_length=128,null=True, blank=True)
	plan = models.CharField(max_length=128,null=True, blank=True)
	currency = models.CharField(max_length=128,null=True, blank=True)
	amount = models.CharField(max_length=128,null=True, blank=True)
	status = models.CharField(max_length=128,null=True, blank=True)
	data = models.JSONField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.id} -- {self.user} -- {self.created_at}"


