from django.contrib import admin
from backend_crud.models import BusStop, Route,Schedule, Bus, Driver, BusSeatStatus
# Register your models here.

admin.site.register([BusStop, Route,Schedule, Bus, Driver, BusSeatStatus])