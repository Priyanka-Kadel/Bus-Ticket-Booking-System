from django import forms
from django.shortcuts import redirect,render
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    full_name=forms.CharField(max_length=100, required=True)
    username=forms.CharField(max_length=25, required=True)
    # contact_number=forms.CharField(max_length=10, required=True)
    password=forms.CharField(max_length=15, min_length=6, required=True)
    confirm_password=forms.CharField(max_length=15, min_length=6, required=True)
    
    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data.get("username")).exists():
            # messages.error(request,"The username you entered is already taken, try another username")
            return redirect ()
        return self.cleaned_data.get("username").strip()
    
    # def clean_contact_number(self):
    #     if User.objects.filter(contact_number=self.cleaned_data.get("contact_number")).exists():
    #         raise forms.ValidationError("This number already exists")
    #     return self.cleaned_data.get("contact_number")
        
    def clean(self):
        if self.cleaned_data.get("password")!=self.cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Password and Confirm password doesn't match")
        return super().clean()
    


class LoginForm(forms.Form):
    username=forms.CharField(max_length=25, required=True)
    password=forms.CharField(max_length=15, min_length=6, required=True)
    
    def clean_username(self):
        return self.cleaned_data.get("username").strip()
        
    