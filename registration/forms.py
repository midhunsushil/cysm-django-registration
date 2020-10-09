from django import forms
from registration.models import Teacher_Info, School_Info, Enquiry_Data

# Create your forms here.

class SchoolForm(forms.ModelForm) :

    class Meta() :
        model = School_Info
        fields = ["school_name", "city", "state", "principal_name", "principal_phone_no", "no_of_students", ]

class TeacherForm(forms.ModelForm) :

    school = forms.ModelChoiceField(School_Info.objects.all(), empty_label="Select your School")
    upload_type = forms.ChoiceField(choices=Teacher_Info.RecordType.choices, initial=Teacher_Info.RecordType.Url, widget=forms.RadioSelect)

    class Meta:
        model = Teacher_Info
        fields = ["school", "full_name", "teacher_id", "phone_no", "upload_type", "url", "upload"]

class EnquiryForm(forms.ModelForm) :

    i_am = forms.ChoiceField(choices = Enquiry_Data.IAmChoices.choices,
                            initial = Enquiry_Data.IAmChoices.staff,
                            widget = forms.HiddenInput(),)

    class Meta():
        model = Enquiry_Data
        fields = ["name", "i_am", "contact_number", "email", "school_name", "school_city", "awareness"]
