from datetime import datetime
from django.shortcuts import render
from backend_crud.forms import search_route
from backend_crud.models import Route, BusSeatStatus, Schedule
from django.db.models import Q, Prefetch
from django.db.models import Count, Case, When, IntegerField


# Create your views here.

def filter_route(request):
    if request.method=='POST':
        search_form = search_route.SearchRouteForm(data=request.POST)
        if search_form.is_valid():
            departure_time_str = search_form.data.get('departure_time')
            departure_time = datetime.strptime(departure_time_str, '%Y-%m-%dT%H:%M')
            # route_obj = Route.objects.prefetch_related(
            #     Prefetch(
            #         'schedule_set',
            #         queryset=Schedule.objects.filter(
            #             departure_time=date_object,
            #             # busseatstatus__available=True
            #         # ).prefetch_related(
            #         #     Prefetch(
            #         #         'busseatstatus_set',
            #         #         queryset=BusSeatStatus.objects.filter(
            #         #             available=True
            #         #         ),
            #         #         to_attr='bus_status'
            #         #     )
            #         ),
            #         to_attr='schedules_with_status'
            #     )
            # )
            schedules_with_buses_and_routes = Schedule.objects.select_related('bus', 'route')\
                .filter(route__to_location=search_form.data.get('to_location'),
                        route__from_location=search_form.data.get('from_location'),
                          departure_time__exact  = departure_time).prefetch_related('busseatstatus_set').annotate(
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
            if  data.get('to_location') not in final_res:
                final_res.append(data.get('to_location'))

        return render(request, 'booking.html', context={'routes':schedules_with_buses_and_routes, 'locations':final_res})
    return render(request, 'booking.html', context={'routes':[]})




