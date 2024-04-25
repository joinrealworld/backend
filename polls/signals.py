from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import post_save
from datetime import timedelta
from polls.models import *
from user.models import *

# @receiver(post_save, sender=MasterPoll)
# def generate_user_polls(sender, instance, created, **kwargs):
#     if created:
#         message = instance.message
#         users = User.objects.all()
#         for user in users:
#         	obj, created = UserPoll.objects.get_or_create(message=message, user=user, master_poll=instance)

