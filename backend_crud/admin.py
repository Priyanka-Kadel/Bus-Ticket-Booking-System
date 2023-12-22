from django.contrib import admin
from backend_crud.models import Route,Schedule, Bus, Driver, BusSeatStatus
# Register your models here.

admin.site.register([Route,Schedule, Bus, Driver, BusSeatStatus])