from django.db import models

# Create your models here.

class BusStop(models.Model):
    stop_name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)

class Route(models.Model):
    from_location = models.CharField(max_length=50)
    to_location = models.CharField(max_length=50)
    route_name = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    stop = models.ForeignKey(BusStop, on_delete=models.CASCADE , null=True, blank=True)

class Driver(models.Model):
    driver_name = models.CharField(max_length=50)
    driver_number = models.CharField(max_length=50)
    lisence_number = models.CharField(max_length=50)
    
class Bus(models.Model):
    bus_number = models.CharField(max_length=50)
    bus_picture = models.ImageField()
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

class Shedule(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()