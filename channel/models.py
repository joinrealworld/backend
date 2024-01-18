import pytz
import random
from datetime import datetime, timedelta
from django.conf import settings
from django.core.validators import ValidationError
from django.db import models
from math import sin, cos, sqrt, atan2, radians
from ckeditor.fields import RichTextField
import string


def category_pic_path(instance, filename):
    return 'category_pic/{}/{}'.format(
        instance.id,
        filename
    )

class Category(models.Model):
    name = models.CharField(max_length=128)
    category_pic = models.ImageField(upload_to=category_pic_path, blank=True, null=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

class Courses(models.Model):
	category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=128,null=True, blank=True)
	data = models.JSONField(null=True, blank=True)

	def __str__(self):
		return f"{self.category.name} -- {self.name}"

class CourseQuiz(models.Model):
	course = models.ForeignKey(Courses, null=True, blank=True, on_delete=models.CASCADE)
	data = models.JSONField(null=True, blank=True)
	index = models.PositiveIntegerField()

	def __str__(self):
		return f"{self.course.name} -- {self.index}"
