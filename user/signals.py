from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import pre_save
from datetime import timedelta
from user.models import EmailVerification  # Import your EmailVerification model

@receiver(pre_save, sender=EmailVerification)
def set_validity(sender, instance, **kwargs):
    if not instance.validity:  # Only set if it's not already set
        instance.validity = timezone.now() + timedelta(hours=24)
