from celery import Celery
from celery.schedules import crontab

from bot import send_jobs
from pytz import timezone


celery_app = Celery("jobs", broker="redis://localhost:6379")

celery_app.conf.beat_schedule = {
    "send_job": {
        "task": "send_job",
        "schedule": crontab(minute=30, hour=8)
    }
}
celery_app.conf.timezone = timezone("Europe/Moscow")


@celery_app.task(name="send_job")
def send_job():
    send_jobs()
