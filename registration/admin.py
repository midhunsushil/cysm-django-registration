from django.contrib import admin
from registration.models import *

# Model admin class
class SchoolAdmin(admin.ModelAdmin) :
    list_display = ('__str__', 'verified')
    list_filter = ('enrolements_to_CS', 'verified')

class TeacherAdmin(admin.ModelAdmin) :
    list_display = ('__str__', 'verified')
    list_filter = ('school', 'verified')

# Register your models here.
# admin.site.register(School_Info)
admin.site.register(School_Info, SchoolAdmin)
admin.site.register(Teacher_Info, TeacherAdmin)
admin.site.register(Enquiry_Data)
admin.site.register(Class_Section)
