import os
import sys

# Add the parent directory of 'streams' (i.e., 'myproject') to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the Django settings module environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django
django.setup()

from streams.scraper import fetch_live_streams

def test_fetch_live_streams():
    streams = fetch_live_streams()
    print(streams)

if __name__ == "__main__":
    test_fetch_live_streams()
