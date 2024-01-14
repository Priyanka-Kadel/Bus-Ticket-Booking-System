from datetime import datetime
from django.shortcuts import render, redirect
from backend_crud.forms import search_route,passenger_form
from backend_crud.models import Route, BusSeatStatus, Schedule, PassengerDetails,PassengerSeat, PaymentDetails
from django.db.models import Q, Prefetch
from django.db.models import Count, Case, When, IntegerField
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from backend_crud.send_mail import send_html_mail




# Create your views here.
def filter_route(request):
    if request.method == 'POST':
        search_form = search_route.SearchRouteForm(data=request.POST)
        if search_form.is_valid():
            departure_date_str = search_form.data.get('departure_time')  
            departure_date = datetime.strptime(departure_date_str, '%Y-%m-%d')

            schedules_with_buses_and_routes = Schedule.objects.select_related('bus', 'route') \
                .filter(route__to_location=search_form.data.get('to_location'),
                        route__from_location=search_form.data.get('from_location'),
                        departure_time__date=departure_date) \
                .prefetch_related('busseatstatus_set') \
                .annotate(
                    available_seats=Count(
                        Case(
                            When(busseatstatus__available=True, then=1),
                            output_field=IntegerField()
                        )
                    )
                )

            route = Route.objects.values('from_location', 'to_location')
            final_res = []
            for data in route:
                if data.get('from_location') not in final_res:
                    final_res.append(data.get('from_location'))
                if data.get('to_location') not in final_res:
                    final_res.append(data.get('to_location'))
    
            return render(request, 'booking.html', context={'routes': schedules_with_buses_and_routes,
                                                          'locations': final_res})
        
    
    print(schedules_with_buses_and_routes)
    return render(request, 'booking.html', context={'routes': []})

def booking_view(request):
    route = Route.objects.values('from_location', 'to_location')
    final_res = []
    for data in route:
        if data.get('from_location') not in final_res:
            final_res.append(data.get('from_location'))
        if  data.get('to_location') not in final_res:
            final_res.append(data.get('to_location'))

    schedules_with_buses_and_routes = Schedule.objects.select_related('bus', 'route') \
        .filter(departure_time__date=datetime.now().date()).prefetch_related('busseatstatus_set') \
        .annotate(
            available_seats=Count(
                Case(
                    When(busseatstatus__available=True, then=1),
                    output_field=IntegerField()
                )
            )
        )
    return render(request,"booking.html", context={"locations":final_res, 'routes': schedules_with_buses_and_routes})


def seats_view(request, route_id):
    schedule = Schedule.objects.select_related('bus', 'route').prefetch_related('busseatstatus_set').filter(id=route_id).annotate(
                available_seats=Count(
                    Case(
                    When(busseatstatus__available=True, then=1),
                    output_field=IntegerField()
                    
                    )
                )
    )  
    schedule=schedule.first()
    busseat =  schedule.busseatstatus_set.all()

    side_a = busseat.filter(seat_side = 'A')
    side_b = busseat.filter(seat_side = 'B')

    
    return render(request, 'seats.html', context={'schedule':schedule,'side_a':side_a, 'side_b': side_b })

@csrf_exempt
def details_views(request):   
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request
            data = json.loads(request.body)

            # Access the values from the JSON data
            scheduled_id = data.get('scheduled_id')
            selected_seats = data.get('selected_seat')
            # Return a JsonResponse with any response data
            response_data = {'data': selected_seats, 'scheduled_id':scheduled_id}
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            # Handle JSON decoding error
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    
    # Handle other HTTP methods if needed
    return JsonResponse({'error': 'Invalid request method'}, status=405)
    

def passenger_details_view (request, id):
    reserved_seats = request.GET.get('seats', None)
    scheduled_id = request.GET.get('scheduled_id', None)
    route = Route.objects.filter(id=id).first()
    return render(request, 'passenger_details.html', context={'route':route, 'reserved_seats':reserved_seats, 'scheduled_id': scheduled_id})

def save_passenger_info(request, id):
    if request.method == 'POST':
        passengerform = passenger_form.PassengerForm(data=request.POST)
        if passengerform.is_valid():
            passenger_form_data = passengerform.cleaned_data
            reserved_seats = passenger_form_data.pop('reserved_seats', '')
            scheduled_id= passenger_form_data.pop('scheduled_id', '')
            if isinstance(reserved_seats, str) and ',' in reserved_seats:
                reserved_seats = reserved_seats.split(',')               
            else:
                reserved_seats= [reserved_seats]
            BusSeatStatus.objects.filter(schedule_id=scheduled_id,id__in=reserved_seats).update(available=False)

            if PassengerSeat.objects.filter(seat_number_id__in=reserved_seats, passenger__schedule__departure_time__date=datetime.now()).exists():
            
                route = Route.objects.filter(id=id).first()
                return render(request, 'passenger_details.html', context={'route':route, 'seat_error':'seats already booked '})

            passenger_detail = PassengerDetails.objects.create(** passenger_form_data)

            for reserved_seat in reserved_seats:
                    PassengerSeat.objects.create(passenger=passenger_detail, seat_number_id = reserved_seat)

            return redirect('payment', id=id, p_id=passenger_detail.id)
        else:
            route = Route.objects.filter(id=id).first()
            return render(request, 'passenger_details.html', context={'route':route, 'error':passengerform.errors})

    route = Route.objects.filter(id=id).first()
    return render(request, 'passenger_details.html', context={'route':route})

def payment_view(request, id, p_id):
    passenger_details = PassengerDetails.objects.filter(schedule__route_id=id, id=p_id, schedule__departure_time__date=datetime.now()).prefetch_related('passengerseat_set', 'paymentdetails_set').first()
    seat_numbers = []
    payment = passenger_details.paymentdetails_set.first()

    if passenger_details:
    # Accessing the passengerseat_set and getting seat numbers
        seat_numbers = [seat.seat_number for seat in passenger_details.passengerseat_set.all()]
    total_price= int(passenger_details.schedule.route.price) * len(seat_numbers)
    return render(request, 'payment.html', context={'passenger_details':passenger_details, 'seat_numbers':seat_numbers, 'total_price':total_price, 'payment':payment})

@csrf_exempt
def verify_payment(request, p_id ):
    data = request.POST
    product_id = data['product_identity']
    token = data['token']
    amount = data['amount']

    url = "https://khalti.com/api/v2/payment/verify/"
    payload = {
    "token": token,
    "amount": amount
    }
    headers = {
    "Authorization": "Key test_secret_key_b6f287aab3874adf880ba3ef82f4471c"
    }
    

    response = requests.post(url, payload, headers = headers)
    
    response_data = json.loads(response.text)
    status_code = str(response.status_code)

    if status_code == '400':
        response = JsonResponse({'status':'false','message':response_data['detail']}, status=500)
        return response

    print(response_data)
    
    payment_method = 'Khalti ' + response_data.get('type')['name']
    passenger_details_instance = PassengerDetails.objects.get(pk=p_id)  # Replace p_id with the actual ID or other identifier
    PaymentDetails.objects.create(passenger_info = passenger_details_instance, payment_method = payment_method, paid_amount= response_data.get('amount'), created_at = response_data.get('created_on'))
    # Fetch the related PassengerSeat instances using prefetch_related
    passenger_seats = PassengerSeat.objects.filter(passenger=passenger_details_instance).select_related('seat_number__schedule__bus')

    # Update the booked status for each related PassengerSeat instance
    for seat in passenger_seats:
        seat.seat_number.booked = True
        seat.seat_number.save()
    send_html_mail([passenger_details_instance.email], passenger_details_instance.id, passenger_details_instance.name)
    return JsonResponse(f"Payment Done !! With IDX. {response_data['user']['idx']}",safe=False)



def ticket_view (request, passenger_id):
    passenger_details_instance = PassengerDetails.objects.filter(pk=passenger_id).select_related('schedule').prefetch_related('passengerseat_set', 'paymentdetails_set').first()
    passenger_seat = passenger_details_instance.passengerseat_set.all()
    schedule = passenger_details_instance.schedule
    payment_details = passenger_details_instance.paymentdetails_set.first()
    return render(request,'ticket.html', context={'passenger_details': passenger_details_instance, 'passenger_seat':passenger_seat, 'schedule':schedule, 'payment_detail':payment_details})


