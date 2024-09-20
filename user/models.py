import pytz
import random
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import ValidationError
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from math import sin, cos, sqrt, atan2, radians
from ckeditor.fields import RichTextField
import string
import uuid
from django.utils import timezone

utc = pytz.UTC

class UserManager(BaseUserManager):
    def create_user(self, username, password):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=self.normalize_email(username),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def avatar_path(instance, filename):
    return 'avatar/{}/{}'.format(
        instance.id,
        filename
    )

def background_path(instance, filename):
    return 'background/{}/{}'.format(
        instance.id,
        filename
    )

class User(AbstractBaseUser):
	THEME_CHOICES = [
		('dark', 'Dark'),
		('light', 'Light'),
	]
	FA_CHOICES = [
		('code', 'Code'),
		('email', 'Email'),
	]
	def save(self, *args, **kwargs):
		if self.pk == None:
			if not (self.email == None or self.email == ""):
				if User.objects.filter(email=self.email).exists():
					return ValidationError("User Already Exist in  this mail id")

			if (self.username == None or self.username == ""):
				first_name = self.first_name
				if first_name:
					username = "_".join(first_name.split(" "))+str(random.randrange(99999, 999999, 12))
					if User.objects.filter(username=username).exists():
						uid = User.objects.last().id + 1
						self.username = f"{username}_{uid}"
					else:
						self.username = f"{username}"

				email = self.email
				if email and not self.username:
					mail_id = email.split("@")[0].lower()
					if User.objects.filter(username=mail_id).exists():
						uid = User.objects.last().id + 1
						self.username = f"{mail_id}_{uid}"
					else:
						self.username = f"{mail_id}"

			self.username = self.username.lower()
			if self.email:
				self.email = self.email.lower()

		super(User, self).save(*args, **kwargs)
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	username = models.CharField(max_length=255, unique=True, blank=False, null=False, )
	email = models.EmailField(blank=True, null=True, unique=True, db_index=True)
	first_name = models.CharField(max_length=255, unique=False, blank=False, null=False, )
	last_name = models.CharField(max_length=255, unique=False, blank=False, null=False, )
	email_otp = models.IntegerField(blank=True, null=True,)
	email_otp_validity = models.DateTimeField(blank=True, null=True,)
	email_verified = models.BooleanField(default=False)
	bio = RichTextField(blank = True)
	invisible = models.BooleanField(default=False)
	status = models.CharField(max_length=255, unique=False, blank=True, null=True, )
	avatar = models.ImageField(upload_to=avatar_path, blank=True, null=True)
	background = models.ImageField(upload_to=background_path, blank=True, null=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	coin = models.PositiveIntegerField(default=500, blank=True, null=True)
	is_online = models.BooleanField(default=False)
	groups = models.ManyToManyField('auth.Group', blank=True, related_name="cutom_user_group")
	referral_code = models.CharField(max_length=128, null=True, blank=True)
	last_login = models.DateTimeField(blank=True, auto_now=True)
	last_coins_award_time = models.DateTimeField(blank=True, null=True)
	theme = models.CharField( max_length=20,choices=THEME_CHOICES,default='dark',)
	sound_effect = models.BooleanField(default=False)
	fa = models.BooleanField(default=False)
	fa_type = models.CharField(max_length=20,choices=FA_CHOICES,default='code',)
	fa_code = models.CharField(max_length=6,null=True, blank=True)
	identity_booster = models.BooleanField(default=False)
	selected_emoji = models.CharField(max_length=128,null=True, blank=True)
	xp = models.IntegerField(default=0)
	level = models.IntegerField(default=1)
	ai_picture = models.CharField(max_length=128, null=True, blank=True)

	objects = UserManager()

	USERNAME_FIELD = "username"

	# REQUIRED_FIELDS = ["username"]

	def set_online_status(self, status):
	    if status == "online":
	        self.is_online = True
	    else:
	        self.is_online = False
	    self.save()

	def has_perm(self, perm, obj=None):
	    user_perms = []
	    if self.is_staff:
	        groups = self.groups.all()
	        for group in groups:
	            perms = [(f"{x.content_type.app_label}.{x.codename}") for x in group.permissions.all()]
	            user_perms += perms

	        if perm in user_perms:
	            return True
	    return (self.is_admin or self.is_superuser)

	def has_module_perms(self, app_label):
	    "Does the user have permissions to view the app `app_label`?"
	    return True

	def get_tokens_for_user(self):
	    refresh = RefreshToken.for_user(self)
	    data = {
	        'refresh': str(refresh),
	        'access': str(refresh.access_token),
	    }	
	    AccessTokenLog.log_access_token(self, str(data['access']))
	    return data

	def generate_random_string(length):
	    characters = string.ascii_letters + string.digits  # include both letters and digits
	    random_string = ''.join(random.choice(characters) for _ in range(length))
	    return random_string

	def verify_2fa_authentication(self, code):
		if self.fa_type == "email":
			fa_verification = FAVerification.objects.filter(email_to__id = self.pk, fa_code = code)
			if fa_verification.exists():
				fa_verification.delete()
				return True
		if self.fa_type == "code":
			if self.fa_code == code:
				return True
		return False

class FAVerification(models.Model):
	email_to = models.ForeignKey(User, on_delete=models.CASCADE, null = False, blank = False)
	fa_code = models.CharField(max_length=255, blank=False, null=False, )
	validity = models.DateTimeField(blank=True, null=True, )

	def validate_email(self, email_to, fa_code):
		# Checking if the email and verification token match the instance
		valid = (self.email_to == email_to and 
				self.fa_code == fa_code and 
				self.validity >= timezone.now())

		# Deleting the instance if validation is successful
		if valid:
			self.delete()

		return valid

class EmailVerification(models.Model):
	email_to = models.ForeignKey(User, on_delete=models.CASCADE, null = False, blank = False)
	verification_token = models.CharField(max_length=255, blank=False, null=False, )
	validity = models.DateTimeField(blank=True, null=True, )

	def validate_email(self, email_to, verification_token):
		# Checking if the email and verification token match the instance
		valid = (self.email_to == email_to and 
				self.verification_token == verification_token and 
				self.validity >= timezone.now())

		# Deleting the instance if validation is successful
		if valid:
			self.delete()

		return valid

class AccessTokenLog(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	token = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)

	@classmethod
	def log_access_token(cls, user, token):
		return cls.objects.create(user=user, token=token)
        
class FeedBack(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	message = RichTextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'Feedback from {self.user.username} at {self.created_at}'

class Referral(models.Model):
    referring_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals', null=True)
    referred_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referred_by', null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.referring_user.username} referred {self.referred_user.username}"

class UserPurchesedEmoji(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	emoji = models.CharField(max_length=255)
	price = models.PositiveIntegerField(default=0)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	selected = models.BooleanField(default=False)

	def __str__(self):
	    return f"{self.id}"

class Tune(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	tune = models.CharField(max_length=255)
	price = models.PositiveIntegerField(default=0)

	def __str__(self):
	    return f"{self.id}"

class UserPurchesedTune(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	tune = models.ForeignKey(Tune, on_delete=models.CASCADE, null=False, blank=False)
	price = models.PositiveIntegerField(default=0)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	selected = models.BooleanField(default=False)

	def __str__(self):
	    return f"{self.id}"

def wallpaper_path(instance, filename):
    return 'wallpaper/{}/{}'.format(
        instance.id,
        filename
    )

class WallPaper(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	wallpaper = models.ImageField(upload_to=wallpaper_path, blank=True, null=True)
	price = models.PositiveIntegerField(default=0)
	timestamp = models.DateTimeField(auto_now_add=True)

class UserWallPaper(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
	wallpaper = models.ForeignKey(WallPaper, on_delete=models.CASCADE, null=False, blank=False)
	is_purchase = models.BooleanField(default=True)
	selected = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
	    return f"{self.id}"

