from django import forms
from .models import Picture
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError
import requests
import shutil
import urllib.request
import os


class UploadImageForm(forms.Form):

    url = forms.URLField(label='URL to image', required=False)
    picture = forms.ImageField(required=False, label='Choose Image')

    def clean(self):
        # Additional condition for fields (Have to choose one and only one of methods)
        cleaned_data = super().clean()
        url_field = cleaned_data.get('url')
        pic_field = cleaned_data.get('picture')

        if url_field and pic_field:
            raise ValidationError('Choose ONLY one of the methods')
        elif not url_field and not pic_field:
            raise ValidationError('Choose AT LEAST one method')


class ResizeImageForm(forms.Form):
    pass
