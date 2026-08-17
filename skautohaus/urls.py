"""
URL configuration for skautohaus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='fnhome'),
    path('service/', views.service, name='fnservice'),
    path('booking/', views.booking, name='fnbooking'),
    path("aboutus/", views.aboutus, name="fnaboutus"),
    path("dashboard/", views.dashboard, name="fndashboard"),
    path("booking-success/<str:booking_id>/", views.booking_success, name="booking_success"),
    path("dashboard/booking/<int:booking_id>/", views.admin_booking_detail, name="admin_booking_detail"),
    path("dashboard/booking/<int:booking_id>/confirm/",views.confirm_booking, name="confirm_booking"),
    path("dashboard/booking/<int:booking_id>/cancel/",views.cancel_booking, name="cancel_booking"),
    path("dashboard/bookings/", views.bookings, name="bookings"),
]
