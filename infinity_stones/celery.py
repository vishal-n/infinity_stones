from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from time import sleep  # For simulating the task duration
from django.utils import timezone
from .models import Activation

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infinity_stones.settings')

app = Celery('infinity_stones')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def stone_activation_task(self, user_id, stone_id, power_duration):
    try:
        # Simulate the start time and end time for activation
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(seconds=power_duration)

        sleep(power_duration)

        # Update the Activation model or perform other relevant logic to mark the activation as complete
        activation = Activation(user_id=user_id, stone_id=stone_id, start_time=start_time, end_time=end_time)
        activation.save()

        return f'Stone activation completed: Stone ID - {stone_id}, User ID - {user_id}, Duration - {power_duration} seconds'
    except Exception as e:
        return f'Error occurred during stone activation: {str(e)}'
