# Generated by Django 3.1.7 on 2021-03-11 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pictures', '0010_remove_picture_picture_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='picture',
            field=models.BinaryField(editable=True),
        ),
    ]
