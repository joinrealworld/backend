from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import pre_save
from datetime import timedelta
from user.models import EmailVerification


@receiver(pre_save, sender=EmailVerification)
def set_validity(sender, instance, **kwargs):
    if not instance.validity:
        instance.validity = timezone.now() + timedelta(hours=24)
