from django import forms
from .models import Booking, Service


class BookingForm(forms.ModelForm):

    booking_time = forms.ChoiceField(
        choices=[
            ("09:00:00", "9:00 AM - 10:00 AM"),
            ("10:00:00", "10:00 AM - 11:00 AM"),
            ("11:00:00", "11:00 AM - 12:00 PM"),
            ("12:00:00", "12:00 PM - 1:00 PM"),
            ("13:00:00", "1:00 PM - 2:00 PM"),
            ("14:00:00", "2:00 PM - 3:00 PM"),
            ("15:00:00", "3:00 PM - 4:00 PM"),
            ("16:00:00", "4:00 PM - 5:00 PM"),
            ("17:00:00", "5:00 PM - 6:00 PM"),
        ],
        widget=forms.Select(attrs={
            "class": "form-input"
        })
    )

    class Meta:
        model = Booking

        fields = [
            "customer_name",
            "customer_email",
            "customer_phone",
            "vehicle_make",
            "vehicle_model",
            "vehicle_year",
            "vehicle_number",
            "service",
            "booking_date",
            "booking_time",
            "message",
        ]

        widgets = {
            "service": forms.Select(attrs={
                "class": "form-input"
            }),

            "booking_date": forms.DateInput(attrs={
                "class": "form-input",
                "type": "date",
            }),
        }