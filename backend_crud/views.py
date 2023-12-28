from datetime import datetime
from django.shortcuts import render, redirect
from backend_crud.forms import search_route,passenger_form
from backend_crud.models import Route, BusSeatStatus, Schedule, PassengerDetails,PassengerSeat
from django.db.models import Q, Prefetch
from django.db.models import Count, Case, When, IntegerField
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json




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
    return render(request, 'booking.html', context={'routes': []})

def booking_view(request):
    route = Route.objects.values('from_location', 'to_location')
    final_res = []
    for data in route:
        if data.get('from_location') not in final_res:
            final_res.append(data.get('from_location'))
        if  data.get('to_location') not in final_res:
            final_res.append(data.get('to_location'))
    return render(request,"booking.html", context={"locations":final_res})


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
            BusSeatStatus.objects.filter(schedule_id=scheduled_id,id__in=selected_seats).update(available=False)
            # Return a JsonResponse with any response data
            response_data = {'data': selected_seats}
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            # Handle JSON decoding error
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    
    # Handle other HTTP methods if needed
    return JsonResponse({'error': 'Invalid request method'}, status=405)
    

def passenger_details_view (request, id):
    reserved_seats = request.GET.get('seats', None)
    route = Route.objects.filter(id=id).first()
    return render(request, 'passenger_details.html', context={'route':route, 'reserved_seats':reserved_seats})

def save_passenger_info(request, id):
    if request.method == 'POST':
        passengerform = passenger_form.PassengerForm(data=request.POST)
        if passengerform.is_valid():
            passenger_form_data = passengerform.cleaned_data
            reserved_seats = passenger_form_data.pop('reserved_seats', '')
            if isinstance(reserved_seats, str) and ',' in reserved_seats:
                reserved_seats = reserved_seats.split(',')               
            else:
                reserved_seats= [reserved_seats]
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
    passenger_details = PassengerDetails.objects.filter(schedule__route_id=id, id=p_id, schedule__departure_time__date=datetime.now()).prefetch_related('passengerseat_set').first()
    seat_numbers = []
    
    if passenger_details:
    # Accessing the passengerseat_set and getting seat numbers
        seat_numbers = [seat.seat_number for seat in passenger_details.passengerseat_set.all()]
    total_price= int(passenger_details.schedule.route.price) * len(seat_numbers)
    return render(request, 'payment.html', context={'passenger_details':passenger_details, 'seat_numbers':seat_numbers, 'total_price':total_price})

