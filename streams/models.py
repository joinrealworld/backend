# models.py
from django.db import models

class Stream(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    is_live = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
