from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from quiz.models import *
from quiz.serializers import *

class QuizStatusSerializer(serializers.Serializer):
    status = serializers.BooleanField()

class QuizScoreSerializer(serializers.ModelSerializer):
	class Meta:
	    model = QuizScore
	    fields = ['uuid', 'user', 'score', 'failer_count', 'created_at']

	# Optionally, you can add custom validation if needed
	def validate_score(self, value):
	    if value < 0:
	        raise serializers.ValidationError("Score must be a positive value.")
	    return value
