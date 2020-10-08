from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime
import os

# Custom Validators and other functions

def number_check(value) :

    try:
        int(value)
        return True
    except ValueError:
        raise ValidationError(
                _('%(value)s is not a valid phone number'),
                params={'value': value},
            )

def user_directory_path(instance, filename):

    #Current datetime strf representation
    currentDateTime = datetime.datetime.now().strftime("%c")
    FILE,EXT = os.path.splitext(filename)
    BASE_DIR = "registration/student_record"
    # file will be uploaded to :
    # MEDIA_ROOT/registration/student_record/instance/<filename>-<currentDateTime><extension>
    return '{0}/{1}/{2}-{3}{4}'.format(BASE_DIR, instance, FILE, currentDateTime, EXT)

# Create your models here.

class School_Info(models.Model) :

    school_name = models.CharField(verbose_name = "School Name", max_length = 100)
    city = models.CharField(max_length = 20)
    state = models.CharField(max_length = 20)
    principal_name = models.CharField(max_length = 100)
    principal_phone_no = models.CharField(max_length = 12, unique = True, validators = [number_check])
    no_of_students = models.PositiveIntegerField()

    def __str__(self):
        return self.school_name

class Teacher_Info(models.Model) :

    # Choices for upload_type
    class RecordType(models.TextChoices):
        Upload = 'Upload', _('Upload File')
        Url = 'URL', _('Spreadsheet URL')

    # Teacher Info
    school = models.ForeignKey(School_Info, on_delete=models.CASCADE)
    full_name = models.CharField(max_length = 100)
    teacher_id = models.CharField(max_length = 20)
    phone_no = models.CharField(max_length = 12, validators = [number_check])
    # Student Records with Teacher
    upload_type = models.CharField(max_length = 10, choices = RecordType.choices, default = RecordType.Url)
    url = models.URLField(blank = True)
    upload = models.FileField(upload_to = user_directory_path, null = True, blank=True)

    def __str__(self):
        # Displays Object in the form "<full_name> (<teacher_id>)"
        return "{0} ({1})".format(self.full_name, self.teacher_id)
