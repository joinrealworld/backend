from rest_framework.serializers import (ModelSerializer,
                                        ValidationError,
                                        )
from rest_framework import serializers
from media_channel.models import *
from content.serializers import ContentSerializer

class MediaChannelSerializer(serializers.ModelSerializer):
	content_id = serializers.IntegerField(required=False, write_only=True) 
	class Meta:
	    model = MediaChannel
	    fields = ['uuid', 'user', 'message', 'content_id', 'content', 'timestamp']
	    read_only_fields = ['uuid', 'timestamp', 'user', 'content']

	def create(self, validated_data):
		# Extract content_id if provided
		content_id = validated_data.pop('content_id', None)
		user = self.context['request'].user

		# Fetch the Content instance if content_id is provided
		if content_id:
			try:
			    content = Content.objects.get(id=content_id)
			except Content.DoesNotExist:
			    raise serializers.ValidationError("Content with the provided ID does not exist.")
			validated_data['content'] = content

		# Create MediaChannel instance
		media_channel = MediaChannel.objects.create(user=user, **validated_data)
		mc_noti = MediaChannelNotifications.objects.create(user = user, media_channel = media_channel)
		return media_channel

class MediaChannelDataSerializer(serializers.ModelSerializer):
	user = serializers.SerializerMethodField()
	content = ContentSerializer(read_only=True)  # Nest the ContentSerializer to get full content details
	likes_count = serializers.SerializerMethodField() 

	class Meta:
		model = MediaChannel
		fields = ['uuid', 'user', 'message', 'content', 'likes_count','timestamp']

	def get_likes_count(self, obj):
		# Return the total number of likes for the MediaChannel instance
		return MediaChannelLike.objects.filter(media_channel=obj).count()

	def get_user(self, instance):
		from user.serializers import UserSimpleSerializer
		return UserSimpleSerializer(instance.user).data

class MediaChannelLikeSerializer(serializers.ModelSerializer):
	media_channel = MediaChannelSerializer()
	user = serializers.SerializerMethodField()

	class Meta:
	    model = MediaChannelLike
	    fields = ['uuid', 'media_channel', 'user', 'timestamp']

	def get_user(self, instance):
		from user.serializers import UserSimpleSerializer
		return UserSimpleSerializer(instance.user).data
        

class MediaNotificationSerializer(serializers.ModelSerializer):
	user = serializers.SerializerMethodField()
	media_channel = MediaChannelSerializer()
	media_channel_like = MediaChannelLikeSerializer()

	class Meta:
	    model = MediaChannelNotifications
	    fields = ['uuid', 'media_channel', 'media_channel_like', 'user', 'timestamp']
	    read_only_fields = ['timestamp']


	def get_user(self, instance):
		from user.serializers import UserSimpleSerializer
		return UserSimpleSerializer(instance.user).data
