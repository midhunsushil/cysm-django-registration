from django.shortcuts import render, redirect
from registration.forms import *
from registration.models import Enquiry_Data, ProfileStatus
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test


# Utility Functions

def mail(SchoolForm) :

    text = "Recieved User Submit ! This needs more work\n"
    values = "School Name: {0}\nPhone: {1}\nEnrolements to CS: {2}".format(SchoolForm.cleaned_data['school_name'], SchoolForm.cleaned_data['contact_number'], SchoolForm.cleaned_data['enrolments_to_CS'])
    from_email = 'midhunpandaraparambilsushil.cs18@bitsathy.ac.in'
    send_mail('User Submit', text+values, from_email, ['midhunpandaraparambilsushil.cs18@bitsathy.ac.in', 'prahladkakkattu@gmail.com'])
    print("Mail sent")

def group_check(user):
    return user.groups.filter(name="Staff | Add School User").exists()

def school_group_check(user):
    return user.groups.filter(name="School").exists()

# Create your views here.

def index(request):

    return render(request, "registration/index.html")

# Enquiry Page
def enquiry_form(request):

    choice = request.GET.get("choice", None)
    choices_list = [t[0] for t in Enquiry_Data.IAmChoices.choices]

    if not choice or choice not in choices_list:
        print("Paramaters not recieved! Redirecting to index page..")
        return HttpResponseRedirect(reverse('index'))

    form = EnquiryForm(initial = {'i_am': choice})

    if request.method == "POST" :

        print("Post Request Recieved !")

        request_data = request.POST.copy()
        request_data.update({'i_am': choice})
        form = EnquiryForm(request_data)

        if form.is_valid() :

            print("Form Data Valid")
            print(form.cleaned_data)
            enquiry_obj = form.save(commit = False)
            token = get_random_string(20)
            enquiry_obj.token = token
            enquiry_obj.save()
            # mail(form)
            # Reset Form
            form = EnquiryForm()
            return redirect('thankyou/')

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
@login_required
@user_passes_test(school_group_check)
def school_reg(request) :

    form_submitted = False
    school_object = request.user.school_info
    form = SchoolForm(instance=school_object)
    formset = class_section_formset(instance=school_object)
    # formset = class_section_formset()

    if request.method == "POST" :

        print("Post Request Recieved !")
        form = SchoolForm(request.POST, instance=school_object)
        formset = class_section_formset(request.POST, instance=school_object)

        if form.is_valid() and formset.is_valid():

            print("Form Data Valid")
            school = form.save()
            formset.save()
            # for _form in formset :
            #     section = _form.save(commit=False)
            #     section.school = school
            #     section.save()

            # mail(form)
            form_submitted = True
            # Reset Form
            form = SchoolForm()

        else :

            print("Form Data Invalid")
            print("form error: ",form.errors)
            print("formset error: ", formset.errors)

    dict = {
        'form' : form,
        'formset' : formset,
        'form_submitted' : form_submitted,
    }
    print(dict['form_submitted'])
    return render(request, "registration/school_registration_page.html", context = dict )

@login_required
@user_passes_test(school_group_check)
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
            teacherObject = form.save(commit=False)
            school_object = request.user.school_info
            teacherObject.school = school_object
            teacherObject.save()

            return index(request)
            # Reset Form
            form = TeacherForm()

        else :

            print("Form Data Invalid")

    dict = {
        'form' : form,
        'form_teacher_details' : [form['full_name'], form['email'], form['contact_number']],
    }
    return render(request, "registration/teacher_registration_page.html", context = dict )

# Register User(School)
@login_required
@user_passes_test(group_check)
def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = SchoolProfileInfoForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid() :

            user = user_form.save()
            user.set_password(user.password)
            school_group = Group.objects.get(name="School")
            user.groups.set([school_group])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            ProfileStatus(school=profile).save()
            registered = True
            user_form = UserForm()
            profile_form = SchoolProfileInfoForm()

        else:
            print(user_form.errors, profile_form.errors)

    else:

        user_form = UserForm()
        profile_form = SchoolProfileInfoForm()

    return render(request, 'registration/register_user(school).html', {
        'user_form' : user_form,
        'profile_form' : profile_form,
        'registered' : registered
    })

@login_required
@user_passes_test(group_check)
def school_profile_status(request):

    profile_status_datas = ProfileStatus.objects.all().order_by('school__school_name')
    return render(request, 'registration/school_profile_status.html', context={
        'profile_status_datas' : profile_status_datas
    })

# User Login Page
def user_login(request) :

    next_page = request.GET.get('next')
    if request.method == "POST" :
        print("POST recieved from user_login!")
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                if next_page :
                    return HttpResponseRedirect(next_page)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account not active!")
        else:
            print("Someone tried to login and failed!")
            print("Username: {} , Password: {}".format(username, password))
            return HttpResponse("invalid login details!")
    else:
        return render(request, 'registration/login.html')

# User Logout Link/Button
def user_logout(request):
    if request.user.is_authenticated :
        logout(request)
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponse("<h1>You must login first to logout!</h1>")
