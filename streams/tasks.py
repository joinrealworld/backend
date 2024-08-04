# streams/tasks.py
from celery import shared_task
from .scraper import fetch_live_streams

@shared_task
def fetch_live_streams_task():
    fetch_live_streams()
