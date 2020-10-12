from django import forms
from django.forms import formset_factory
from registration.models import Teacher_Info, School_Info, Enquiry_Data, Class_Section

# Create your forms here.

class SchoolForm(forms.ModelForm) :

    class Meta() :
        model = School_Info
        fields = ["school_name", "school_code", "contact_number", "enrolements_to_CS", "no_of_teachers", ]

class ClassSectionForm(forms.ModelForm) :

    class Meta() :
        model = Class_Section
        fields = ["class_no", "section", "teacher_email", "contact_number"]

# Formset of above Form
class_section_formset = formset_factory(ClassSectionForm, extra = 1)

class TeacherForm(forms.ModelForm) :

    school = forms.ModelChoiceField(School_Info.objects.all(), empty_label="Select your School")
    school_code = forms.CharField(initial = "School Code", widget = forms.TextInput(attrs={'readonly':'readonly', 'class':'disabled'}))
    upload_type = forms.ChoiceField(choices=Teacher_Info.RecordType.choices, initial=Teacher_Info.RecordType.Url, widget=forms.RadioSelect)

    class Meta:
        model = Teacher_Info
        fields = ["school", "full_name", "contact_number", "upload_type", "url", "upload"]

class EnquiryForm(forms.ModelForm) :

    i_am = forms.ChoiceField(choices = Enquiry_Data.IAmChoices.choices,
                            initial = Enquiry_Data.IAmChoices.staff,
                            widget = forms.HiddenInput(),)

    class Meta():
        model = Enquiry_Data
        fields = ["name", "i_am", "contact_number", "email", "school_name", "school_city", "awareness"]
