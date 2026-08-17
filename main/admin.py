from django.contrib import admin
from .models import Service, Booking


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "duration", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "booking_id",
        "customer_name",
        "customer_phone",
        "service",
        "booking_date",
        "booking_time",
        "status",
    )

    list_filter = ("status", "service", "booking_date")
    search_fields = (
        "booking_id",
        "customer_name",
        "customer_phone",
        "vehicle_make",
        "vehicle_model",
        "vehicle_number",
    )

    ordering = ("-created_at",)