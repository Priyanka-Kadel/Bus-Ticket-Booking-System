from django.urls import path
from . import views
from .views import home, register_view, login_view, admin_pannel_view
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path(' ', views.home, name='home'),  # This is the default view for the root URL
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin_pannel/', admin_pannel_view, name='login'),
    
]
