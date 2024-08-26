from django.db import models
from user.models import User
import uuid
from content.models import Content

class BlackhallChat(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    message = models.JSONField(null=True, blank=True)
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