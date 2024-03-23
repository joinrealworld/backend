from rest_framework import serializers
from rest_framework.serializers import (ModelSerializer,
                                        )
from user.models import *
from django.contrib.auth.password_validation import validate_password
from payment.models import *

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
    customer_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'uuid','avatar', 'email','background', 'theme', 'fa', 'fa_type', 'username', 'first_name', 'last_name', 'bio','email_verified', 'status', 'invisible', 'customer_id','referral_code')

    def get_avatar(self, obj):
        return obj.avatar.url if obj.avatar else obj.dummy_avatar

    def get_customer_id(self, obj):
        try:
            return CustomerDetails.objects.filter(user = obj).last().customer_id
        except Exception as e:
            print("get_customer_id serializer method exception -->", e)
            return ""


class ChangeInvisibleSerializer(serializers.Serializer):
    invisible = serializers.BooleanField()

class ChangeStatusSerializer(serializers.Serializer):
    status = serializers.CharField(allow_blank=True)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

class AvatarSerializer(serializers.Serializer):
    avatar = serializers.ImageField()

class UploadAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('avatar',)

class BackgroundSerializer(serializers.Serializer):
    background = serializers.ImageField()

class UploadBackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('background',)

class ChangeBioSerializer(serializers.Serializer):
    bio = serializers.CharField(max_length=500, allow_blank=True)

class FeedbackSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=255, required=True)

class UpdateThemeSerializer(serializers.Serializer):
    theme = serializers.ChoiceField(choices=User.THEME_CHOICES)

class UpdateSoundEffectSerializer(serializers.Serializer):
    sound_effect = serializers.BooleanField()

class UpdateAuthenticationSerializer(serializers.Serializer):
    authentication = serializers.BooleanField(required = True)
    authentication_type = serializers.ChoiceField(choices=User.FA_CHOICES, required = False)
    authentication_code = serializers.CharField(max_length=6, required=False)

    

