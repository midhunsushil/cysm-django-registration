from django.contrib import admin
from registration.models import *
from django.utils.translation import gettext_lazy as _

# Filter Class
class EnrolmentListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('enrolments')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'enrolments_to_CS'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('<100', _('Less than 100')),
            ('100-300', _('100 - 300')),
            ('300-600', _('300 - 600')),
            ('600<', _('More than 600')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == '<100':
            return queryset.filter(enrolments_to_CS__lt=100)
        if self.value() == '100-300':
            return queryset.filter(enrolments_to_CS__gte=100,
                                    enrolments_to_CS__lte=300)
        if self.value() == '300-600':
            return queryset.filter(enrolments_to_CS__gte=300,
                                    enrolments_to_CS__lte=600)
        if self.value() == '600<':
            return queryset.filter(enrolments_to_CS__gt=600)




# Model admin class
class SchoolAdmin(admin.ModelAdmin) :
    # list_display = ('__str__', 'verified')
    list_filter = (EnrolmentListFilter,)

class TeacherAdmin(admin.ModelAdmin) :
    list_display = ('__str__', 'verified')
    list_filter = ('school', 'verified')

# Register your models here.
# admin.site.register(School_Info)
admin.site.register(School_Info, SchoolAdmin)
admin.site.register(Teacher_Info, TeacherAdmin)
admin.site.register(Enquiry_Data)
admin.site.register(Class_Section)
admin.site.register(ProfileStatus)
