from datetime import datetime
from django.shortcuts import render
from backend_crud.forms import search_route
from backend_crud.models import Route, BusSeatStatus, Schedule
from django.db.models import Q, Prefetch

# Create your views here.

def filter_route(request):
    if request.method=='POST':
        print (request.POST)
        search_form = search_route.SearchRouteForm(data=request.POST)
        if search_form.is_valid():
            date_object = datetime.strptime(search_form.data.get('departure_time'), '%Y-%m-%d')
            route_obj = Route.objects.prefetch_related(
                Prefetch(
                    'schedule_set',
                    queryset=Schedule.objects.filter(
                        departure_time__date=date_object,
                        busseatstatus__available=True
                    ).prefetch_related(
                        Prefetch(
                            'busseatstatus_set',
                            queryset=BusSeatStatus.objects.filter(
                                available=True
                            ),
                            to_attr='bus_status'
                        )
                    ),
                    to_attr='schedules_with_status'
                )
            ).filter(
                Q(to_location=search_form.data.get('to_location')) &
                Q(from_location=search_form.data.get('from_location'))
            )

            for route in route_obj:
                print(f"Route: {route}")
                #Iterate through the related Schedule objects
                for schedule in route.schedule_set.all():
                    print(f"  Schedule: {schedule.departure_time}")

                    # # Access the related BusSeatStatus instances
                    # for seat_status in schedule.bus_status:
                    #     print(f"    BusSeatStatus: {seat_status.seat_number}, Available: {seat_status.available}, Booked: {seat_status.booked}")

    return render(request, 'home.html')




