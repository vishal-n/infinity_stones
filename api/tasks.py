# infinity_stones/tasks.py
from celery import shared_task
from time import sleep
from django.utils import timezone
from .models import Activation

@shared_task
def activate_stone(user_id, stone_id, power_duration):
    # Simulate the start time and end time for activation
    start_time = timezone.now()
    end_time = start_time + timezone.timedelta(seconds=power_duration)

    # Perform the stone activation task
    sleep(power_duration)

    # Update the Activation model or perform other relevant logic to mark the activation as complete
    activation = Activation(user_id=user_id, stone_id=stone_id, start_time=start_time, end_time=end_time)
    activation.save()

    return f'Stone activation completed: Stone ID - {stone_id}, User ID - {user_id}, Duration - {power_duration} seconds'
