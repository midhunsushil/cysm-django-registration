# Generated by Django 3.1.1 on 2020-10-20 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0012_auto_20201020_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enquiry_data',
            name='token',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
