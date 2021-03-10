from django.db import models
import os


# Create your models here.
class Picture(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=50, null=True)

    # Image info
    picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')

    # picture = models.ImageField(upload_to='images') # Если хотим хранить изображения в форме изображений

    def __str__(self):
        return self.file_name
