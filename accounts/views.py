from django.shortcuts import render,redirect
from accounts.account_forms import RegisterForm, LoginForm
# from django.contrib import messages
from accounts.service.account_write import  create_user
from django.contrib.auth import login, logout


# Create your views here.
def register_view(request):
    register_form=RegisterForm
    if request.method =='POST':
        data = request.POST
        form_data = register_form(data)
        if form_data.is_valid():
            user = create_user(form_data.cleaned_data)
            login(request, user)
            return redirect("login")
        else:
            print(register_form.errors)
        print (form_data.errors)

        # messages.error(request,"The username you entered is already taken, try another username")

    return render(request,"account/register.html")

def login_view(request):
    register_form=LoginForm
    if request.method =='POST':
        data = request.POST
        form_data = register_form(data)
        if form_data.is_valid():
            return redirect("home")
        else:
            print(register_form.errors)
        print (form_data.errors)
    return render(request, "account/login.html")

def logout_view(request):
    logout(request)
    return render(request, 'account/login.html')

def home_view(request):
    return render(request, 'home.html')





