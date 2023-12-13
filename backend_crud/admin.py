from django.contrib import admin
from backend_crud.models import BusStop, Route,Shedule, Bus, Driver
# Register your models here.

admin.site.register([BusStop, Route,Shedule, Bus, Driver])