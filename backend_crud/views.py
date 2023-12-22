from datetime import datetime
from django.shortcuts import render
from backend_crud.forms import search_route
from backend_crud.models import Route, BusSeatStatus, Schedule
from django.db.models import Q, Prefetch
from django.db.models import Count, Case, When, IntegerField


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

    print(busseat)
    return render(request, 'seats.html', context={'schedule':schedule,'side_a':side_a, 'side_b': side_b })

def details_views(request):   
    return render(request, 'details.html')




