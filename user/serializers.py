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
    username = serializers.SerializerMethodField()
    # selected_emoji = serializers.SerializerMethodField()
    selected_tune = serializers.SerializerMethodField()
    selected_wallpaper = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'uuid','avatar', 'email', 'identity_booster','background', 'coin','theme', 'fa', 'is_admin','fa_type', 'is_online','username', 'first_name', 'last_name', 'bio','email_verified', 'status', 'invisible', 'customer_id','referral_code', 'selected_emoji','selected_tune', 'selected_wallpaper')

    def get_avatar(self, obj):
        return obj.avatar.url if obj.avatar else obj.dummy_avatar

    def get_username(self, obj):
        return obj.username+obj.selected_emoji if obj.selected_emoji else obj.username

    def get_customer_id(self, obj):
        try:
            return CustomerDetails.objects.filter(user = obj).last().customer_id
        except Exception as e:
            print("get_customer_id serializer method exception -->", e)
            return ""

    # def get_selected_emoji(self, obj):
    #     user_emoji = UserPurchesedEmoji.objects.filter(user = obj, selected = True)
    #     if user_emoji.exists():
    #         return user_emoji.last().emoji
    #     return ""

    def get_selected_tune(self, obj):
        user_tune = UserPurchesedTune.objects.filter(user = obj, selected = True)
        if user_tune.exists():
            return user_tune.last().tune
        return ""

    def get_selected_wallpaper(self, obj):
        user_wallpaper = UserWallPaper.objects.filter(user = obj, selected = True)
        if user_wallpaper.exists():
            return user_wallpaper.last().wallpaper.wallpaper.url
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

class PurchesEmojiSerializer(serializers.Serializer):
    emoji = serializers.CharField()
    price = serializers.IntegerField()

    def validate_price(self, value):
        if value <= 0:
            raise ValidationError("Price must be a positive integer.")
        return value

class PurchesTuneSerializer(serializers.Serializer):
    tune = serializers.CharField()
    price = serializers.IntegerField()

    def validate_price(self, value):
        if value <= 0:
            raise ValidationError("Price must be a positive integer.")
        return value

class UserPurchesedEmojiSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPurchesedEmoji
        fields = ['id', 'uuid','emoji', 'price', 'selected','timestamp']

class TuneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tune
        fields = "__all__"

class UserPurchesedTuneSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPurchesedTune
        fields = ['id', 'uuid','tune', 'price', 'selected','timestamp']

class WallPaperSerializer(serializers.ModelSerializer):
    is_purchase = serializers.SerializerMethodField()
    selected = serializers.SerializerMethodField()

    class Meta:
        model = WallPaper
        fields = ['id', 'uuid','wallpaper', 'price', 'is_purchase', 'selected']

    def get_is_purchase(self, obj):
        user = self.context.get('user')
        if user:
            return UserWallPaper.objects.filter(user=user, wallpaper=obj).exists()
        return False

    def get_selected(self, obj):
        user = self.context.get('user')
        if user:
            user_wallpaper = UserWallPaper.objects.filter(user=user, wallpaper=obj).first()
            if user_wallpaper:
                return user_wallpaper.selected
        return False
