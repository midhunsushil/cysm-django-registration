from django import forms
from django.forms import inlineformset_factory, formset_factory
from registration.models import Teacher_Info, School_Info, Enquiry_Data, Class_Section
from django.contrib.auth.models import User

# Create your forms here.

class SchoolForm(forms.ModelForm) :

    class Meta() :
        model = School_Info
        fields = ["school_name", "school_code", "contact_number", "enrolments_to_CS", "no_of_teachers", ]

class ClassSectionForm(forms.ModelForm) :

    class Meta() :
        model = Class_Section
        fields = ["class_no", "section", "teacher_email", "contact_number"]

# Formset of above Form
# class_section_formset = formset_factory(ClassSectionForm, extra = 1)
class_section_formset = inlineformset_factory(School_Info, Class_Section,
    fields=("class_no", "section", "teacher_email", "contact_number"),
    extra=1, can_delete=True)

class TeacherForm(forms.ModelForm) :

    upload_type = forms.ChoiceField(choices=Teacher_Info.RecordType.choices, initial=Teacher_Info.RecordType.Url, widget=forms.RadioSelect)

    class Meta:
        model = Teacher_Info
        fields = ["full_name", "email", "contact_number", "upload_type", "url", "upload"]

class EnquiryForm(forms.ModelForm) :

    i_am = forms.ChoiceField(choices = Enquiry_Data.IAmChoices.choices,
                            initial = Enquiry_Data.IAmChoices.staff,
                            widget = forms.HiddenInput(),)

    class Meta():
        model = Enquiry_Data
        fields = ["name", "i_am", "contact_number", "email", "school_name", "school_city", "awareness",]

class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class SchoolProfileInfoForm(forms.ModelForm):

    class Meta:
        model = School_Info
        fields = ['school_name', 'contact_number']
