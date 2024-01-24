from django.db import models
from django.core.exceptions import ValidationError


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
    def clean(self):
        if not self.driver_number.isdigit():
            raise ValidationError("Number must contain only digits")

        if len(self.driver_number) != 10:
            raise ValidationError("Number must be 10 characters long")
        
        for char in self.lisence_number:
            if not (char.isdigit() or char == '-'):
                raise ValidationError("License number must contain only digits ")
    
class Bus(models.Model):
    bus_number = models.CharField(max_length=50)
    bus_picture = models.ImageField()
    total_seat = models.IntegerField(default=0)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.bus_number}"
    
    def clean(self):
        existing_bus = Bus.objects.filter(bus_number=self.bus_number).exclude(pk=self.pk)
        if existing_bus.exists():
            raise ValidationError("Bus with this number already exists.")
        
        if self.total_seat > 20:
            raise ValidationError("Maximum seat of our bus is 20")
            

class Schedule(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    def __str__(self):
        return f"{self.bus.bus_number} - {self.departure_time}"
    
    def clean(self):
        # Check if the same bus is scheduled on the same day for a different route
        existing_schedule = Schedule.objects.filter(
            bus=self.bus,
            departure_time__date=self.departure_time.date(),
        ).exclude(pk=self.pk)

        if existing_schedule.exists():
            raise ValidationError("This bus is already scheduled for another route on the same day.")
        
        
class BusSeatStatus(models.Model):
    CHOICES = [
        ('A', 'Side A'),
        ('B', 'Side B'),
    ]
    seat_side = models.CharField(max_length=1, choices=CHOICES, default='A')

    seat_number = models.IntegerField()
    available = models.BooleanField(default=True)
    booked = models.BooleanField(default=False)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.schedule.bus.bus_number} - {self.seat_number}"
    
    def clean(self):
        # Check if the seat is being created or updated
        is_creation = self._state.adding
        # If it's a new instance, or if it's an update and the seat is available,
        if is_creation or (not self.available and is_creation):
        # Ensure that the total number of seats in BusSeatStatus
            if self.schedule.busseatstatus_set.count() >= self.schedule.bus.total_seat:
                raise ValidationError("Cannot add more seats than the total seat")

    class Meta:
        ordering = ['seat_side','seat_number']

    

class PassengerDetails(models.Model):
    name = models.CharField(max_length=25)
    contact = models.CharField(max_length=10)
    email = models.EmailField()
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, blank=True , null= True)

    def __str__(self):
        return f"{self.name} ({self.email})"
    
    def clean(self):
        if not self.contact.isdigit():
            raise ValidationError("Contact must contain only digits")

        if len(self.contact) != 10:
            raise ValidationError("Contact must be 10 characters long")
        
    
class PassengerSeat(models.Model):
    passenger = models.ForeignKey(PassengerDetails, on_delete=models.CASCADE)    
    seat_number = models.ForeignKey(BusSeatStatus, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.passenger.name} ( {self.seat_number})"
    

class PaymentDetails(models.Model):
    passenger_info = models.ForeignKey(PassengerDetails, on_delete=models.CASCADE)  
    payment_method = models.CharField(max_length= 25, default = "Khalti")
    paid_amount = models.CharField(max_length= 25)
    created_at = models.DateTimeField()

    def __str__(self):
        return f"{self.passenger_info.name}({self.passenger_info.email}) "