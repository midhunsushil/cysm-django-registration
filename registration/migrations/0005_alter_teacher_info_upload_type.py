# Generated by Django 3.2 on 2021-05-13 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_profilestatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher_info',
            name='upload_type',
            field=models.CharField(choices=[('URL', 'Spreadsheet URL'), ('Upload', 'Upload File')], default='URL', max_length=10),
        ),
    ]
