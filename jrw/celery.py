# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jrw.settings.settings')

app = Celery('jrw')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Ensure that your task modules are discovered
app.autodiscover_tasks(['streams'])
