from django.shortcuts import render, redirect
from registration.forms import *
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail

# Create your views here.

def index(request):

    return render(request, "registration/index.html")

# Enquiry Page
def enquiry_form(request):

    choice = request.GET['choice']
    form = EnquiryForm(initial = {'i_am': choice})

    if request.method == "POST" :

        print("Post Request Recieved !")
        data = {
            'name': request.POST['name'],
            'contact_number': request.POST['contact_number'],
            'email': request.POST['email'],
            'school_name': request.POST['school_name'],
            'school_city': request.POST['school_city'],
            'awareness': request.POST['awareness'],
            'i_am': choice
        }
        print(data)
        form = EnquiryForm(data)

        if form.is_valid() :

            print("Form Data Valid")
            form.save()
            # mail(form)
            return redirect('thankyou/')
            # Reset Form
            form = EnquiryForm()

        else :

            print("Form Data Invalid")
            errors = dict(form.errors)
            print(errors)

    data = {
        'form' : form,
    }
    return render(request, "registration/enquiry_form_page.html", context = data )

def thankyou_enquiry(request) :

    return render(request, "registration/thank_you.html")

# School Registration Form
def school_reg(request) :

    form = SchoolForm()
    formset = class_section_formset()

    if request.method == "POST" :

        print("Post Request Recieved !")
        form = SchoolForm(request.POST)
        formset = class_section_formset(request.POST)

        if form.is_valid() and formset.is_valid():

            print("Form Data Valid")
            school = form.save()
            for _form in formset :
                section = _form.save(commit=False)
                section.school = school
                section.save()

            mail(form)
            return index(request)
            # Reset Form
            form = SchoolForm()

        else :

            print("Form Data Invalid")

    dict = {
        'form' : form,
        'formset' : formset,
    }
    return render(request, "registration/school_registration_page.html", context = dict )


def teacher_reg(request) :

    form = TeacherForm()

    if request.GET.get('school_id'):

        school_id = request.GET.get('school_id')
        school_code = School_Info.objects.get(pk = school_id).school_code
        return HttpResponse(school_code)

    if request.method == "POST" :

        print("Post Request Recieved !")
        form = TeacherForm(request.POST, request.FILES)

        if form.is_valid() :

            print("Form Data Valid")
            form.save()
            return index(request)
            # Reset Form
            form = TeacherForm()

        else :

            print("Form Data Invalid")

    dict = {
        'form' : form,
        'form_teacher_details' : [form['school'], form['school_code'], form['full_name'], form['email'], form['contact_number']],
    }
    return render(request, "registration/teacher_registration_page.html", context = dict )

def mail(SchoolForm) :

    text = "Recieved User Submit ! This needs more work\n"
    values = "School Name: {0}\nPhone: {1}\nEnrolements to CS: {2}".format(SchoolForm.cleaned_data['school_name'], SchoolForm.cleaned_data['contact_number'], SchoolForm.cleaned_data['enrolements_to_CS'])
    send_mail('User Submit', text+values, 'iAmRoony@cysm-dev.xyz', ['wewovo6066@deselling.com', 'midhunpandaraparambilsushil.cs18@bitsathy.ac.in', 'prahladkakkattu@gmail.com'])
    print("Mail sent")
