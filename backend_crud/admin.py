from django.contrib import admin
from backend_crud.models import Route,Schedule, Bus, Driver, BusSeatStatus
from backend_crud.forms.admin.admin_form import BusSeatStatusAdminForm
# Register your models here.

class BusSeatStatusAdmin(admin.ModelAdmin):
    form = BusSeatStatusAdminForm

admin.site.register(BusSeatStatus, BusSeatStatusAdmin)

admin.site.register([Route,Schedule, Bus, Driver])
