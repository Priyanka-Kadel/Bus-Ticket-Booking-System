from django.urls import path
from backend_crud.views import filter_route,seats_view,details_views,booking_view,save_passenger_info,payment_view,passenger_details_view,verify_payment,ticket_view



urlpatterns = [  
    path('filter-route/', filter_route, name='route'),
    path('booking/', booking_view, name='booking'),
    path('seats/<int:route_id>/', seats_view, name='seats'),
    path('details/', details_views, name='details'),
    path('passenger-details/<int:id>/', passenger_details_view, name='passenger-details'),
    path('create-passenger/<int:id>/', save_passenger_info, name='create-passenger'),
    path('payment/<int:id>/<int:p_id>/', payment_view, name='payment'),

    path('api/verify_payment/<int:p_id>/',verify_payment,name='verify_payment'),
    path('ticket/<int:passenger_id>/', ticket_view, name='ticket'),

]
