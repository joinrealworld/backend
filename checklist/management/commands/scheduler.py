from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.core.management.base import BaseCommand
from checklist.models import MasterCheckList, UserDailyCheckList
from user.models import User
from django.utils import timezone
import pytz
import time

def create_copy_daily_checklist():
    master_checklist = MasterCheckList.objects.all()  # Adjust as per your logic
    users = User.objects.all()

    for checklist in master_checklist:
        UserDailyCheckList.objects.create(
            master_checklist=checklist,
        )
        checklist.copied_at = timezone.now()
        checklist.save()

    print('Daily checklists copied successfully! '+ str(timezone.now()))