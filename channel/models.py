import pytz
import random
from datetime import datetime, timedelta
from django.conf import settings
from django.core.validators import ValidationError
from django.db import models
from math import sin, cos, sqrt, atan2, radians
from ckeditor.fields import RichTextField
import string
import uuid
from user.models import User

def category_pic_path(instance, filename):
    return 'category_pic/{}/{}'.format(
        instance.id,
        filename
    )

def course_pic_path(instance, filename):
    return 'course_pic/{}/{}'.format(
        instance.id,
        filename
    )

def master_category_pic_path(instance, filename):
    return 'master_category_pic/{}/{}'.format(
        instance.id,
        filename
    )

class MasterCategory(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=128)
	category_pic = models.FileField(upload_to=master_category_pic_path, blank=True, null=True)
	description = RichTextField(blank = True)

	def __str__(self):
	    return f"{self.name}"

class Category(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=128)
	category_pic = models.ImageField(upload_to=category_pic_path, blank=True, null=True)
	description = RichTextField(blank = True)
	master_category =  models.ForeignKey(MasterCategory, null=True, blank=True, on_delete=models.CASCADE)

	def __str__(self):
	    return f"{self.name}"


class Courses(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=128,null=True, blank=True)
	data = models.JSONField(null=True, blank=True)
	is_favorite = models.BooleanField(default=False)
	description = RichTextField(blank = True)
	pic = models.ImageField(upload_to=course_pic_path, blank=True, null=True)

	def __str__(self):
		return f"{self.category.name} -- {self.name}"

class CourseQuiz(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	course = models.ForeignKey(Courses, null=True, blank=True, on_delete=models.CASCADE)
	data = models.JSONField(null=True, blank=True)
	index = models.PositiveIntegerField()

	def __str__(self):
		return f"{self.course.name} -- {self.index}"

class FavoriteCourseContent(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	course = models.ForeignKey(Courses, null=False, blank=False, on_delete=models.CASCADE)
	user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
	content_uuid = models.CharField(max_length=128,null=False, blank=False)
	
	def __str__(self):
		return f"{self.course.name} -- {self.user.id}"

class FavoriteCourse(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	course = models.ForeignKey(Courses, null=False, blank=False, on_delete=models.CASCADE)
	user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
	
	def __str__(self):
		return f"{self.course.name} -- {self.user.id}"

class CompleteContent(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	course = models.ForeignKey(Courses, null=False, blank=False, on_delete=models.CASCADE)
	user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
	content_uuid = models.CharField(max_length=128,null=False, blank=False)
	
	def __str__(self):
		return f"{self.course.name} -- {self.user.id}"
