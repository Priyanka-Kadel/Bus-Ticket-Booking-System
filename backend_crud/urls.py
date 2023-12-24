from django.urls import path
from backend_crud.views import filter_route,seats_view,details_views,booking_view,save_passenger_info


urlpatterns = [  
    path('filter-route/', filter_route, name='route'),
    path('booking/', booking_view, name='booking'),
    path('seats/<int:route_id>/', seats_view, name='seats'),
    path('details/', details_views, name='details'),
    path('create-passenger/', save_passenger_info, name='create-passenger'),

]
