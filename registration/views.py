from django.shortcuts import render
from registration.forms import *
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail

# Create your views here.

def index(request):

    return render(request, "registration/index.html")

def school_reg(request) :

    form = SchoolForm()

    if request.method == "POST" :

        print("Post Request Recieved !")
        form = SchoolForm(request.POST)

        if form.is_valid() :

            print("Form Data Valid")
            form.save()
            mail(form)
            return index(request)
            # Reset Form
            form = SchoolForm()

        else :

            print("Form Data Invalid")

    dict = {
        'form' : form,
    }
    return render(request, "registration/school_registration_page.html", context = dict )


def teacher_reg(request) :

    form = TeacherForm()

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
        'form_teacher_details' : [form['school'], form['full_name'], form['teacher_id'], form['phone_no']],
    }
    return render(request, "registration/teacher_registration_page.html", context = dict )

def mail(SchoolForm) :

    text = "Recieved User Submit ! This needs more work\n"
    values = "School Name: {0}\nCity: {1}\nPrincipal Name: {2}\nPhone: {3}".format(SchoolForm.cleaned_data['school_name'], SchoolForm.cleaned_data['city'], SchoolForm.cleaned_data['principal_name'], SchoolForm.cleaned_data['principal_phone_no'])
    send_mail('User Submit', text+values, 'iAmRoony@cysm-dev.xyz', ['reber23046@zuperholo.com', 'prahladkakkattu@gmail.com'])
    print("Mail sent")

def test(request) :

    print("sending mail")
    send_mail('test', 'this is a test message', 'iAmRoony@cysm-dev.xyz', ['reber23046@zuperholo.com', 'prahladkakkattu@gmail.com'])

    return HttpResponse("Hi")
