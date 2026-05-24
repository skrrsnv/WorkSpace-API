from celery import shared_task
from .models import ActivityLog


@shared_task
def create_activity_log(user_id, action_type, payload=None):
    ActivityLog.objects.create(user_id=user_id, action_type=action_type, payload=payload or {})
