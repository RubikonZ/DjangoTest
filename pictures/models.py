from django.db import models
import os
from django.core.files import File
from tempfile import NamedTemporaryFile
import urllib.request


# Create your models here.
class Picture(models.Model):
    parent_picture = models.ImageField(upload_to='images/parent_pictures', )
    picture_name = models.CharField(max_length=50, null=True)
    picture = models.ImageField(upload_to='images')
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')

    def __str__(self):
        return self.picture_name
