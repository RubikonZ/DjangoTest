# Generated by Django 3.1.7 on 2021-03-11 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pictures', '0008_picture_content_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='picture',
            old_name='file_name',
            new_name='picture_name',
        ),
    ]
