# streams/views.py
from django.http import JsonResponse
from .models import Stream

def live_streams_api(request):
    print("live_streams_api view called")  # Debug print statement
    streams = Stream.objects.values('server_name', 'title', 'start_time', 'end_time', 'is_live')
    return JsonResponse(list(streams), safe=False)