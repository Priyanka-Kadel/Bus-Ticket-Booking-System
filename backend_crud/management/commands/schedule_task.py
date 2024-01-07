from django.core.management.base import BaseCommand
import schedule
import time
from backend_crud.models import PassengerSeat
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from django.db import transaction


class Command(BaseCommand):
    help = 'Run scheduled task'

    def handle(self, *args, **options):
        # Define your task logic here
        def your_scheduled_task():
            print("Scheduled task executed!")
            # Get the current time
            current_time = timezone.now()
            # Calculate the time 5 minutes ago
            five_minutes_ago = current_time - timedelta(minutes=1)
            ten_minutes_ago = five_minutes_ago - timedelta(minutes=1)


            # Query for passenger seats created before 5 minutes
            passenger_seats_before_5_min = PassengerSeat.objects.filter(
                created_at__gte=ten_minutes_ago,
                created_at__lte=five_minutes_ago,
                seat_number__booked=False,
                seat_number__available=False
            ).select_related('passenger')          
            print(passenger_seats_before_5_min)
            # Print or use the results as needed

            with transaction.atomic():

                for passenger_seat in passenger_seats_before_5_min:
                    passenger_detail = passenger_seat.passenger
                    bus_seat_status = passenger_seat.seat_number
                    bus_seat_status.available=True
                    bus_seat_status.save()
                    passenger_detail.delete()
            
                passenger_seats_before_5_min.delete()

        # Schedule the task to run every 60 seconds
        schedule.every(5).seconds.do(your_scheduled_task)


        # Run the scheduler loop
        while True:
            schedule.run_pending()
            time.sleep(1)
