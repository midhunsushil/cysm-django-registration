from django import forms

class User_Reg(forms.Form) :

    full_name = forms.CharField(max_length = 50)
    email = forms.EmailField(max_length = 100)
