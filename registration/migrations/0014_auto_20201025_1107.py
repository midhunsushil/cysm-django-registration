# Generated by Django 3.1.1 on 2020-10-25 05:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0013_auto_20201020_2144'),
    ]

    operations = [
        migrations.AddField(
            model_name='class_section',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 25, 5, 37, 38, 890392, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='enquiry_data',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 25, 5, 37, 38, 891765, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='school_info',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 25, 5, 37, 38, 889395, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='teacher_info',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 25, 5, 37, 38, 890461, tzinfo=utc)),
        ),
    ]