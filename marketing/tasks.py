from celery import shared_task
from .utils import send_sms
from .models import Marketing
from django.utils.timezone import now


@shared_task
def send_marketing_sms(marketing_id):
    """
    Sends SMS for a specific Marketing campaign to its target audiences and updates status to 'working'.
    """
    try:
        print(f"Task started for marketing ID: {marketing_id}")
        marketing = Marketing.objects.get(id=marketing_id)

        # Update status to 'working' when the task starts
        marketing.status = 'working'
        marketing.save()

        # Send SMS
        to = list(marketing.target_audiences.values_list('phone_number', flat=True))
        message = marketing.message
        response = send_sms(to, message)

        return {"status": "success", "response": response}
    except Marketing.DoesNotExist:
        return {"status": "error", "message": "Marketing not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@shared_task
def send_end_marketing_sms(marketing_id):
    """
    Sends an ending SMS for a specific Marketing campaign and updates status to 'done'.
    """
    try:
        print(f"Task started for marketing ID: {marketing_id}")
        marketing = Marketing.objects.get(id=marketing_id)

        # Send SMS
        to = list(marketing.target_audiences.all().values_list('phone_number', flat=True))
        message = f"{marketing.message}\n تنها 2 روز ازین کمپین باقی مانده است"

        response = send_sms(to, message)

        # Check if the campaign has ended and update status to 'done'
        if marketing.end_date <= now():
            marketing.status = 'done'
            marketing.save()

        return {"status": "success", "response": response}
    except Marketing.DoesNotExist:
        return {"status": "error", "message": "Marketing not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

