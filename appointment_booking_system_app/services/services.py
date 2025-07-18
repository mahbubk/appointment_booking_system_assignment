from datetime import timedelta

from django.core.mail import send_mail
from django.db.models import Count, Sum
from django.utils.timezone import now

from appointment_booking_system_app.models import (
    Appointment,
    AppointmentReminder,
    MonthlyReport,
)


def send_24_hour_reminders():
    tomorrow = now().date() + timedelta(days=1)
    appointments = Appointment.objects.filter(
        appointment_date=tomorrow, status="confirmed"
    )

    for appointment in appointments:
        if AppointmentReminder.objects.filter(
            appointment=appointment, reminder_type="24_hours", is_sent=True
        ).exists():
            continue

        send_mail(
            subject="Appointment Reminder",
            message=f"Dear {appointment.patient.fullname}, you have an appointment with Dr. {appointment.doctor.user.fullname} on {appointment.appointment_date} at {appointment.appointment_time}.",
            from_email="clinic@example.com",  # dummy email
            recipient_list=[appointment.patient.email],  # dummy email
            fail_silently=True,
        )

        AppointmentReminder.objects.create(
            appointment=appointment, reminder_type="24_hours", is_sent=True
        )


def generate_reports_for_last_month():
    today = now().date()
    first_day_this_month = today.replace(day=1)
    last_month = first_day_this_month - timedelta(days=1)
    year, month = last_month.year, last_month.month

    appointments = (
        Appointment.objects.filter(
            appointment_date__year=year,
            appointment_date__month=month,
            status="completed",
        )
        .values("doctor")
        .annotate(
            total_appointments=Count("id"),
            total_patients=Count("patient", distinct=True),
            total_earnings=Sum("consultation_fee"),
        )
    )

    for data in appointments:
        MonthlyReport.objects.update_or_create(
            doctor_id=data["doctor"],
            year=year,
            month=month,
            defaults={
                "total_appointments": data["total_appointments"],
                "total_patients": data["total_patients"],
                "total_earnings": data["total_earnings"] or 0,
            },
        )
