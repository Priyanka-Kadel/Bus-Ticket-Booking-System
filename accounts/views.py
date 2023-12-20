from django.shortcuts import render,redirect
from accounts.account_forms import RegisterForm, LoginForm
# from django.contrib import messages
from accounts.service.account_write import  create_user
from django.contrib.auth import login, logout
from backend_crud.models import Route

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

# def logout_view(request):
#     logout(request)
#     return render(request, 'account/login.html')

def home_view(request):
    return render(request, 'home.html')

def booking_view(request):
    route = Route.objects.values('from_location', 'to_location')
    final_res = []
    for data in route:
        if data.get('from_location') not in final_res:
            final_res.append(data.get('from_location'))
        if  data.get('to_location') not in final_res:
            final_res.append(data.get('to_location'))
    return render(request,"booking.html", context={"locations":final_res})



def seats_view(request, route_name, bus_number, from_location, to_location, departure_time, total_seat, available_seats, price):
    # You can use these parameters to display information in the seats.html template
    return render(request, 'seats.html', {
        'route_name': route_name,
        'bus_number': bus_number,
        'from_location': from_location,
        'to_location': to_location,
        'departure_time': departure_time,
        'total_seat': total_seat,
        'available_seats': available_seats,
        'price': price,
    })

