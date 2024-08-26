from rest_framework.serializers import (ModelSerializer,
                                        ValidationError,
                                        )
from rest_framework import serializers
from content.models import *


class UploadContentSerializer(serializers.ModelSerializer):
    content_name = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = (
            'id', 
            'type_of_content', 
            'content_name', 
            'channel_type', 
            'content', 
            'thumbnail', 
            'extention', 
            'duration'
        )

    def create(self, validated_data):
        # Fetch the current user from the request context
        user = self.context['request'].user

        # Create a new Content instance with the validated data
        content = Content(**validated_data)

        # Assign the uploader to the current user
        content.uploader = user
        
        # Save the content instance
        content.save()
        
        return content

    def get_content_name(self, data):
        # Safely extract the file name from the content field
        return data.content.name.split("/")[-1] if data.content else None


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'type_of_content', 'content', 'extention', 'duration', 'thumbnail', 'channel_type']