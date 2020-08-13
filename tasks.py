from celery import Celery
from celery.schedules import crontab

from bot import send_jobs


celery_app = Celery("jobs")

celery_app.conf.beat_schedule = {
    "send_job": {
        "task": "send_job",
        "schedule": crontab(minute=0, hour=12)
    }
}


@celery_app.task(name="send_job")
def send_job():
    send_jobs()
