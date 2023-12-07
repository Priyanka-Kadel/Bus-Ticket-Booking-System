from django.urls import path
from homeview.views import home_page

urlpatterns = [
    path('', home_page, name='home'),    
]