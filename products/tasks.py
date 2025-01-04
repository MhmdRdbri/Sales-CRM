from celery import shared_task

@shared_task
def print_text():
    print("This text is printed every 30 seconds.")