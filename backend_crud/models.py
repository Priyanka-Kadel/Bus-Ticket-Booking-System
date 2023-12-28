from django.db import models


class Route(models.Model):
    from_location = models.CharField(max_length=50)
    to_location = models.CharField(max_length=50)
    route_name = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.from_location} - {self.to_location}"

class Driver(models.Model):
    driver_name = models.CharField(max_length=50)
    driver_number = models.CharField(max_length=50)
    lisence_number = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.driver_name}"
    
class Bus(models.Model):
    bus_number = models.CharField(max_length=50)
    bus_picture = models.ImageField()
    total_seat = models.IntegerField(default=0)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.bus_number}"


class Schedule(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    def __str__(self):
        return f"{self.bus.bus_number} - {self.departure_time}"
    
class BusSeatStatus(models.Model):
    CHOICES = [
        ('A', 'Side A'),
        ('B', 'Side B'),
    ]
    seat_side = models.CharField(max_length=1, choices=CHOICES, default='A')

    seat_number = models.CharField(max_length=50)
    available = models.BooleanField(default=True)
    booked = models.BooleanField(default=False)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.schedule.bus.bus_number} - {self.seat_number}"
    
class PassengerDetails(models.Model):
    name = models.CharField(max_length=25)
    contact = models.CharField(max_length=10)
    email = models.EmailField()
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, blank=True , null= True)

    def __str__(self):
        return self.email
    
class PassengerSeat(models.Model):
    passenger = models.ForeignKey(PassengerDetails, on_delete=models.CASCADE)    
    seat_number = models.ForeignKey(BusSeatStatus, on_delete=models.CASCADE)
