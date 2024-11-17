from rest_framework import serializers
from raffel.models import Raffel
import random
from django.utils.timezone import now

class RaffelSerializer(serializers.ModelSerializer):
    total_index = serializers.SerializerMethodField()

    class Meta:
        model = Raffel
        fields = ['uuid', 'user', 'index', 'total_index', 'timestamp']  # Specify the fields to be serialized

    def get_total_index(self, obj):
        try:
            today = now().date()
            return (Raffel.objects.filter(timestamp__date=today).first().total_index)
        except Exception as e:
            return 0
