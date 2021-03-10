from django import forms
from .models import Picture
from django.core.files.uploadedfile import InMemoryUploadedFile


class CreateForm(forms.ModelForm):
    #max_upload_limit = 2 * 1024 * 1024

    # Call this 'picture' so it gets copied from the form to the in-memory model
    # It will not be the "bytes", it will be the "InMemoryUploadedFile"
    # because we need to pull out things like content_type
    picture = forms.FileField(required=True, label='Выбрать')
    upload_field_name = 'picture'
    # picture = forms.ImageField(required=True, label=Выбрать') # Если хотим хранить изображения в форме изображений
    #upload_field_name = 'picture'

    class Meta:
        model = Picture
        fields = ['picture']

    # Конвертирую файл в изображение
    def save(self, commit=True):
        instance = super(CreateForm, self).save(commit=False)

        f = instance.picture
        if isinstance(f, InMemoryUploadedFile):
            byte_img = f.read()
            instance.content_type = f.content_type
            instance.picture = byte_img

        if commit:
            instance.save()
        return instance
