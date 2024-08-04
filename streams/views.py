# streams/views.py
from django.http import JsonResponse
from .models import Stream

def live_streams_api(request):
    print("live_streams_api view called")  # Debug print statement
    streams = Stream.objects.filter(is_live=True).values('title', 'url')
    return JsonResponse(list(streams), safe=False)