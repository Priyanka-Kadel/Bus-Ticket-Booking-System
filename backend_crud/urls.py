from django.urls import path
from backend_crud.views import filter_route


urlpatterns = [  
    path('filter-route/', filter_route, name='route'),

]
