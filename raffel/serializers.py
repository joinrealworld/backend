from rest_framework import serializers
from raffel.models import Raffel

class RaffelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Raffel
        fields = ['uuid', 'user', 'index', 'timestamp']  # Specify the fields to be serialized
