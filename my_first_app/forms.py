from django import forms
from my_first_app.models import Login

# Create your models here.

class Login_form(forms.Form):

    username = forms.CharField(min_length=8, widget=forms.TextInput(attrs={"placeholder":"Email Address"}))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={"placeholder" : "Password"}))
    botcheck = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean(self):

        cleaned_data = super().clean()

        print(cleaned_data)
        print(self.errors)

        if cleaned_data['botcheck']:
            print("\u001b[31;1mBOT DETECTION ALERT !\u001b[0m")
            raise forms.ValidationError("Please RELOAD Page")

        # self.verify_user_login(clean_data)

    def verify_user_login(self):

        uname = self.cleaned_data['username']
        passwd = self.cleaned_data['password']
        login_object = Login.objects.filter(username=uname)
        print("Object:",login_object)
        username_exists = login_object.exists()

        if not username_exists:
            self.add_error('__all__', forms.ValidationError("Username or Password does not Exist !"))
            print("\u001b[31;1mUsername or Password does not Exist !\u001b[0m")
            return forms.ValidationError("Username or Password does not Exist !")

        else:

            if not login_object[0].password == passwd :

                self.add_error('__all__', forms.ValidationError("Invaild Password. Please try again..."))
                print("\u001b[31;1mInvaild Password. Please try again...\u001b[0m")
                # raise forms.ValidationError("Invaild Password. Please try again...")
                return forms.ValidationError("Invaild Password. Please try again...")

            else:

                return True
