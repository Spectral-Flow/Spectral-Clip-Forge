"""
Celery Worker Configuration for Background Processing
The forge's eternal flames, always burning, always ready
"""
from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Celery
celery = Celery(
    "spectral_clip_forge",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
    include=["tasks.video_processor"],
)

# Celery configuration
celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=int(os.getenv("JOB_TIMEOUT", 600)),
    worker_max_tasks_per_child=50,
    worker_prefetch_multiplier=1,
)

if __name__ == "__main__":
    celery.start()
