from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import BookingForm
from .models import Booking,  Service
import uuid
from django.utils import timezone  
from django.core.mail import send_mail 
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def dashboard(request):
    today = timezone.localdate()

    bookings = Booking.objects.all()

    todays_bookings = Booking.objects.filter(
        booking_date=today
    ).count()

    pending_bookings = Booking.objects.filter(
        status="pending"
    ).count()

    confirmed_bookings = Booking.objects.filter(
        status="confirmed"
    ).count()

    completed_bookings = Booking.objects.filter(
        status="completed"
    ).count()

    cancelled_bookings = Booking.objects.filter(
        status="cancelled"
    ).count()

    todays_schedule = Booking.objects.filter(
        booking_date=today
    ).order_by("booking_time")

    return render(request,"dashboard.html",
        {
            "bookings": bookings,
            "todays_bookings": todays_bookings,
            "pending_bookings": pending_bookings,
            "confirmed_bookings": confirmed_bookings,
            "completed_bookings": completed_bookings,
            "cancelled_bookings": cancelled_bookings,
            "todays_schedule": todays_schedule,
        }
    )

@login_required
def admin_booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    return render(
        request,
        "booking_detail.html",
        {
            "booking": booking,
        }
    )


def booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)

            # Generate a unique booking ID
            booking.booking_id = "SK-" + uuid.uuid4().hex[:8].upper()

            booking.save()

            return redirect("booking_success", booking_id=booking.booking_id)

    else:
        form = BookingForm()

    return render(request, "booking.html", {"form": form})

def booking_success(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id)

    return render(request,"booking_success.html",{"booking": booking})


def home(request):
    return render(request, 'home.html')

def service(request):
    return render(request, 'services.html')


def aboutus(request):
    return render(request, 'aboutus.html')

@login_required
def bookings(request):

    bookings = Booking.objects.all()

    pending_bookings = Booking.objects.filter(
        status="pending"
    ).count()

    confirmed_bookings = Booking.objects.filter(
        status="confirmed"
    ).count()

    cancelled_bookings = Booking.objects.filter(
        status="cancelled"
    ).count()

    return render(
        request,
        "bookings.html",
        {
            "bookings": bookings,
            "pending_bookings": pending_bookings,
            "confirmed_bookings": confirmed_bookings,
            "cancelled_bookings": cancelled_bookings,
        }
    )

@login_required
def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == "POST":

        # Change booking status
        booking.status = "confirmed"
        booking.save()

        # Send confirmation email
        if booking.customer_email:
            send_mail(
                subject="SK AutoHaus - Booking Confirmed",
                message=f"""
Dear {booking.customer_name},

Your booking with SK AutoHaus has been confirmed.

BOOKING DETAILS
-------------------------
Booking ID: {booking.booking_id}

Service: {booking.service.name}

Vehicle: {booking.vehicle_make} {booking.vehicle_model}

Date: {booking.booking_date.strftime("%d %B %Y")}

Time: {booking.booking_time.strftime("%I:%M %p")}

Status: CONFIRMED
-------------------------

Please arrive at SK AutoHaus at your scheduled time.

Thank you for choosing SK AutoHaus.

SK AutoHaus
Kollam, Kerala
""",
                from_email=None,
                recipient_list=[booking.customer_email],
                fail_silently=False,
            )

        messages.success(
            request,
            f"Booking {booking.booking_id} confirmed successfully."
        )

        return redirect(
            "admin_booking_detail",
            booking_id=booking.id
        )

    return redirect(
        "admin_booking_detail",
        booking_id=booking.id
    )

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == "POST":
        reason = request.POST.get("cancellation_reason", "").strip()

        # Change booking status
        booking.status = "cancelled"
        booking.cancellation_reason = reason
        booking.save()

        # Send cancellation email
        if booking.customer_email:
            send_mail(
                subject="SK AutoHaus - Booking Cancelled",
                message=f"""
Dear {booking.customer_name},

Your booking with SK AutoHaus has been cancelled.

BOOKING DETAILS
-------------------------

Booking ID: {booking.booking_id}

Service: {booking.service.name}

Vehicle: {booking.vehicle_make} {booking.vehicle_model}

Date: {booking.booking_date.strftime("%d %B %Y")}

Time: {booking.booking_time.strftime("%I:%M %p")}

Status: CANCELLED

Cancellation Reason:
{booking.cancellation_reason}

-------------------------

If you have any questions or would like to book another appointment,
please contact SK AutoHaus.

Thank you.

SK AutoHaus
Kollam, Kerala
""",
                from_email=None,
                recipient_list=[booking.customer_email],
                fail_silently=False,
            )

        messages.success(
            request,
            f"Booking {booking.booking_id} cancelled successfully."
        )

        return redirect(
            "admin_booking_detail",
            booking_id=booking.id
        )

    return redirect(
        "admin_booking_detail",
        booking_id=booking.id
    )