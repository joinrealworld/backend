from blackhall.models import *
from rest_framework import serializers
from rest_framework.response import Response
from django.urls import reverse
from django.conf import settings
import string
import random
from user.models import User

class BlackHallSerializer(serializers.ModelSerializer):

	class Meta:
		model = BlackhallChat
		fields = ('uuid','user', 'message', 'timestamp')
