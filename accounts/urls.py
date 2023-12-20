from django.urls import path
from .views import register_view, login_view, booking_view, home_view, seats_view
# from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home_view, name='home'),  # Use 'home' as the name for the root URL
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('booking/', booking_view, name='booking'),
    path('seats/<str:route_name>/<str:bus_number>/<str:from_location>/<str:to_location>/<str:departure_time>/<int:total_seat>/<int:available_seats>/<int:price>/', seats_view, name='seats'),
]
