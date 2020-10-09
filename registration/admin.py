from django.contrib import admin
from registration.models import School_Info, Teacher_Info, Enquiry_Data

# Register your models here.
admin.site.register(School_Info)
admin.site.register(Teacher_Info)
admin.site.register(Enquiry_Data)
