""" Celery Implementation """
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "appointment_booking_system.settings")

app = Celery("appointment_booking_system")


app.config_from_object("django.conf:settings", namespace="CELERY")


app.autodiscover_tasks()

app.conf.beat_schedule = {
    "send-daily-reminders": {
        "task": "appointment_booking_system_app.tasks.send_daily_appointment_reminders",
        "schedule": crontab(hour=8, minute=0),  # Every day at 8 AM
    },
    "generate-monthly-report": {
        "task": "appointment_booking_system_app.tasks.generate_monthly_reports",
        "schedule": crontab(
            day_of_month=1, hour=2, minute=0
        ),  # 1st of each month at 2 AM
    },
}

""" Background Jobs(celery) """
# celery -A appointment_booking_system worker --loglevel=info
# celery -A appointment_booking_system beat --loglevel=info
