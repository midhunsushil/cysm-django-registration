from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
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
    # File will be uploaded to MEDIA_ROOT/registration/student_record/instance/<filename>-<currentDateTime><extension>
    return '{0}/{1}/{2}-{3}{4}'.format(BASE_DIR, instance.full_name, FILE, currentDateTime, EXT)

# Create your models here.

class School_Info(models.Model) :

    school_name = models.CharField(verbose_name = "School Name", max_length = 100)
    school_code = models.CharField(max_length = 20)
    # city = models.CharField(max_length = 20)
    # state = models.CharField(max_length = 20)
    # principal_name = models.CharField(max_length = 100)
    contact_number = models.CharField(max_length = 12, unique = True, validators = [number_check])
    enrolments_to_CS = models.PositiveIntegerField()
    no_of_teachers = models.PositiveIntegerField()
    created_at = models.DateTimeField(default = timezone.now, editable = True, blank = True)
    verified = models.BooleanField(default = False)

    def __str__(self):
        return self.school_name

class Class_Section(models.Model) :

    school = models.ForeignKey(School_Info, on_delete=models.CASCADE)
    class_no = models.PositiveIntegerField(verbose_name = "Class")
    section = models.CharField(max_length = 3)
    teacher_email = models.EmailField(max_length = 50)
    contact_number = models.CharField(max_length = 12, validators = [number_check])
    created_at = models.DateTimeField(default = timezone.now, editable = True, blank = True)

    def __str__(self) :
        # Displays Object in the form "<class_>-<section>"
        school_name = str(self.school)
        return "{0}-{1}@{2}".format(self.class_no, self.section, school_name)

class Teacher_Info(models.Model) :

    # Choices for upload_type
    class RecordType(models.TextChoices):
        Upload = 'Upload', _('Upload File')
        Url = 'URL', _('Spreadsheet URL')

    # Teacher Info
    school = models.ForeignKey(School_Info, on_delete=models.CASCADE)
    full_name = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 50)
    contact_number = models.CharField(max_length = 12, validators = [number_check])
    # Student Records with Teacher
    upload_type = models.CharField(max_length = 10, choices = RecordType.choices, default = RecordType.Url)
    url = models.URLField(blank = True)
    upload = models.FileField(upload_to = user_directory_path, null = True, blank=True)

    verified = models.BooleanField(default = False)
    created_at = models.DateTimeField(default = timezone.now, editable = True, blank = True)

    def __str__(self):
        # Displays Object in the form "<full_name> (<teacher_id>)"
        return "{0}@{1}".format(self.full_name, str(self.school))

class Enquiry_Data(models.Model) :

    # Choices for upload_type
    class IAmChoices(models.TextChoices):
        principal = 'Principal', _('Principal')
        teacher = 'Teacher', _('Teacher')
        student = 'Student', _('Student')
        staff = 'Staff', _('Staff')

    name = models.CharField(verbose_name = "Name*", max_length = 100)
    i_am = models.CharField(max_length = 10, choices = IAmChoices.choices, default = IAmChoices.staff)
    contact_number = models.CharField(verbose_name = "Contact Number*", max_length = 12, validators = [number_check])
    email = models.EmailField(verbose_name = "Email*", max_length = 50)
    school_name = models.CharField(verbose_name = "School Name*", max_length = 100)
    school_city = models.CharField(verbose_name = "School City*", max_length = 20)
    awareness = models.CharField(verbose_name = "Where did you hear about us ?", max_length = 100, blank = True)
    token = models.CharField(max_length = 20, unique = True)
    created_at = models.DateTimeField(default = timezone.now, editable = True, blank = True)

    def __str__(self):
        # Displays Object in the form "<IAmChoice>@<school_name>"
        return "{0}".format(self.token)
