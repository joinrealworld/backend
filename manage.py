# #!/usr/bin/env python
# """Django's command-line utility for administrative tasks."""
# import os
# import sys
# import time
# from threading import Thread
# from django.core.management import execute_from_command_line
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.cron import CronTrigger
# import pytz
# from django.utils import timezone


# def check_and_copy_checklist():
#     from checklist.models import UserDailyCheckList
#     from checklist.management.commands.scheduler import create_copy_daily_checklist 
#     last_entry = UserDailyCheckList.objects.order_by('-created_at').first()
#     if last_entry:
#         # Check if the last entry was copied today
#         today = timezone.now().date()
#         last_entry_date = last_entry.created_at.date()
#         if last_entry_date != today:
#             create_copy_daily_checklist()
#     else:
#         create_copy_daily_checklist()

# def start_scheduler():
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jrw.settings.settings')  # Adjust settings module path
    
#     import django
#     django.setup()  # Initialize Django application
    
#     from checklist.management.commands.scheduler import create_copy_daily_checklist  # Import after Django setup
#     scheduler = BackgroundScheduler(timezone=pytz.timezone('America/Toronto'))
#     scheduler.add_job(check_and_copy_checklist, CronTrigger(hour=0, minute=0))  # Run daily at 12 AM
#     # scheduler.add_job(check_and_copy_checklist, CronTrigger(second='*/10'))  # Run every 10 sec
#     scheduler.start()

#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         scheduler.shutdown()

# def main():
#     """Run administrative tasks."""
#     try:
#         execute_from_command_line(sys.argv)
#     except Exception as exc:
#         print(f"An error occurred: {exc}")
#         sys.exit(1)

# if __name__ == '__main__':
#     scheduler_thread = Thread(target=start_scheduler)
#     scheduler_thread.daemon = True  # Daemonize the scheduler thread
#     scheduler_thread.start()

#     main()  # Run Django's command-line utility

#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jrw.settings.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

    


if __name__ == '__main__':
    main()