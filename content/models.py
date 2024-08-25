from django.db import models
from user.models import User


def content_upload_path(instance, filename):
    return 'content/{0}/{1}/{2}/{3}'.format(
        instance.uploader.id,
        instance.channel_type,
        instance.type_of_content,
        filename
        )


def thumbnail_upload_path(instance, filename):
    return 'content/thumbnail/{0}/{1}/{2}/{3}'.format(
        instance.uploader.id,
        instance.channel_type,
        instance.type_of_content,
        filename
        )

class Content(models.Model):
    """ Content model for storing all types of contents """

    TYPE_OF_CONTENT = (
                            ("image", "Image"),
                            ("docs", "Docs"),
                            ("video", "Video"),
                            ("audio", "Audio"),
                            ("sticker", "Sticker"),
                           )

    CHANNEL_TYPE = (
    		("blackhall", "Blackhall"),
    	)

    uploader = models.ForeignKey("user.User", on_delete=models.CASCADE,
                             limit_choices_to={"is_active": True})
    type_of_content = models.CharField(max_length=10,
                                        choices=TYPE_OF_CONTENT,
                                        )
    content = models.FileField(upload_to=content_upload_path)
    extention = models.CharField(max_length=50, blank=True, null=True)
    duration = models.CharField(max_length=10, blank=True, null=True)
    thumbnail=models.ImageField(upload_to=thumbnail_upload_path, blank=True, null=True)
    channel_type = models.CharField(max_length=10,
                                        choices=CHANNEL_TYPE,
                                        )
