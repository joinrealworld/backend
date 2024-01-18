from rest_framework import serializers
from rest_framework.serializers import (ModelSerializer,
                                        )
from user.models import *

class EmailLoginSerializer(ModelSerializer):
    """ Login Serializer """

    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'email': {'required': True}
        }

class UserSimpleSerializer(ModelSerializer):
    """ User Basic Information Serializer """

    class Meta:
        model = User
        fields = ('id', 'avatar', 'username', 'first_name', 'last_name','email_verified', 'referral_code')

    def get_avatar(self, obj):
        return obj.avatar.url if obj.avatar else obj.dummy_avatar