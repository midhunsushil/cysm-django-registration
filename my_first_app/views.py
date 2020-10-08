from django.shortcuts import render
from django.http import HttpResponse
from my_first_app.models import Login
from my_first_app.forms import Login_form
import emoji

# Create your views here.
def index(request):
    dict = {'var_para':"Bubblegum Sans is upbeat, flavor-loaded, brushalicious letters for the sunny side of the street. It bounces with joy and tells a great story.",
        'login_records': Login.objects.all().order_by('username')
    }
    return render(request, 'my_first_app/index.html', context=dict)

def login(request):
    form = Login_form()

    if request.method == "POST" :

        print("POST Request Recieved⬇️")
        form = Login_form(request.POST)
        print(request.POST)

        if form.is_valid():

            print("Form Data Validated ✔️")
            print(form.cleaned_data)
            print("Starting User Verification")

            if form.verify_user_login() == True:

                print("\u001b[32;1mUser Login Verified !\u001b[0m✔️")

        else:

            print("Form Data Invalid ❌")
            errors = dict(form.errors)
            # print(form.non_field_errors())
            print(errors)


    return render(request, 'my_first_app/login.html', context = {"form": form})
