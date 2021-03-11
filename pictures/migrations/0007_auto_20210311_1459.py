# Generated by Django 3.1.7 on 2021-03-11 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pictures', '0006_picture_file_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='picture',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='picture',
            name='created_at',
        ),
        migrations.AddField(
            model_name='picture',
            name='picture_url',
            field=models.URLField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='picture',
            name='picture',
            field=models.ImageField(upload_to='images'),
        ),
    ]
