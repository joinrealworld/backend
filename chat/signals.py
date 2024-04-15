from chat.models import *
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver

#
#
# @receiver(post_save, sender=Message)
# def set_message_read(sender, instance, created, **kwargs):
#     if created: