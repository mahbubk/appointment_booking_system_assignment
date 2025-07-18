""" tasks.py """
from celery import shared_task

from appointment_booking_system_app.services.services import (
    generate_reports_for_last_month,
    send_24_hour_reminders,
)


@shared_task
def send_daily_appointment_reminders():
    send_24_hour_reminders()


@shared_task
def generate_monthly_reports():
    generate_reports_for_last_month()
