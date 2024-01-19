from celery import shared_task
from django.core.management import call_command
from requests.exceptions import HTTPError


@shared_task
def task_load_data():
    try:
        call_command('load_data')
    except HTTPError as e:
        # Handle specific errors related to DALL-E or other HTTP requests
        print(f"HTTP error occurred: {e}")
    except Exception as e:
        # Handle any other exceptions
        print(f"An error occurred: {e}")
