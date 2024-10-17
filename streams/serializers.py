from rest_framework import serializers
from .models import Stream

class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = ['server_name', 'title', 'start_time', 'end_time']
