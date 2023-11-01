from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from time import sleep
from django.utils import timezone
from .models import Activation

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infinity_stones.settings')

app = Celery('infinity_stones')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def stone_activation_task(self, user_id, stone_id, power_duration):
    try:
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(seconds=power_duration)

        sleep(power_duration)

        activation = Activation(user_id=user_id, stone_id=stone_id, start_time=start_time, end_time=end_time)
        activation.save()

        return f'Stone activation completed: Stone ID - {stone_id}, User ID - {user_id}, Duration - {power_duration} seconds'
    except Exception as e:
        return f'Error occurred during stone activation: {str(e)}'
