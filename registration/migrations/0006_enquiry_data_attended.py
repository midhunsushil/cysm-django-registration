# Generated by Django 3.2 on 2021-06-09 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_alter_teacher_info_upload_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiry_data',
            name='attended',
            field=models.BooleanField(default=False),
        ),
    ]
