from datetime import datetime
from django.shortcuts import render, redirect
from backend_crud.forms import search_route,passenger_form
from backend_crud.models import Route, BusSeatStatus, Schedule, PassengerDetails
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
            response_data = {'message': 'Request processed successfully'}
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            # Handle JSON decoding error
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    
    # Handle other HTTP methods if needed
    return JsonResponse({'error': 'Invalid request method'}, status=405)
    

def passenger_details_view (request, id):
    route = Route.objects.filter(id=id).first()
    return render(request, 'passenger_details.html', context={'route':route})

def save_passenger_info(request, id):
    if request.method == 'POST':
        passengerform = passenger_form.PassengerForm(data=request.POST)
        if passengerform.is_valid():
            PassengerDetails.objects.create(** passengerform.cleaned_data)
            return render(request , 'payment.html')
        else:
            print(passengerform.errors)
            route = Route.objects.filter(id=id).first()
            return render(request, 'passenger_details.html', context={'route':route, 'error':passengerform.errors})

    route = Route.objects.filter(id=id).first()
    return render(request, 'passenger_details.html', context={'route':route})

def payment_view(request):
   return render(request, 'payment.html')
