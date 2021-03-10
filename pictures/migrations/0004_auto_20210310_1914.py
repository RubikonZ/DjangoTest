# Generated by Django 3.1.7 on 2021-03-10 16:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pictures', '0003_picture_content_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='picture',
            name='content_type',
        ),
        migrations.AddField(
            model_name='picture',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='picture',
            name='picture',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='pictures'),
            preserve_default=False,
        ),
    ]