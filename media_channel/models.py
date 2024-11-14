from django.db import models
from user.models import User
import uuid
from content.models import Content
from ckeditor.fields import RichTextField

# Create your models here.
class MediaChannel(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	message = RichTextField(blank = True)
	content = models.ForeignKey(Content, null = True, blank=True, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)

	class Meta:
	    ordering = ['-timestamp']
	    indexes = [
	        models.Index(fields=['timestamp']),
	        models.Index(fields=['user']),
	    ]

	def __str__(self):
	    message_preview = (self.message[:20] + '...') if isinstance(self.message, str) and len(self.message) > 20 else self.message
	    return f"Chat by {self.user} at {self.timestamp}: {message_preview}"


class MediaChannelLike(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
	media_channel = models.ForeignKey(MediaChannel, null = False, blank=False, on_delete=models.CASCADE)
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)
	

	class Meta:
	    ordering = ['-timestamp']
	    indexes = [
	        models.Index(fields=['timestamp']),
	        models.Index(fields=['user']),
	    ]
	    constraints = [
            models.UniqueConstraint(fields=['media_channel', 'user'], name='unique_media_like')
        ]

class MediaChannelNotifications(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
	media_channel = models.ForeignKey(MediaChannel, null=True, blank=True, on_delete=models.CASCADE)
	media_channel_like = models.ForeignKey(MediaChannelLike, null=True, blank=True, on_delete=models.CASCADE)
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)

	class Meta:
	    ordering = ['-timestamp']

