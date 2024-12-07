from celery import shared_task
from .utils import send_sms
from .models import Marketing


@shared_task
def send_marketing_sms(marketing_id):
    """
    Sends SMS for a specific Marketing campaign to its target audiences.
    """
    try:
        print(f"Task started for marketing ID: {marketing_id}")
        marketing = Marketing.objects.get(id=marketing_id)

        # Correctly access related target audiences using the instance
        to = list(marketing.target_audiences.values_list('phone_number', flat=True))
        message = marketing.message
        print(f"Target audiences manager: {marketing.target_audiences}")
        print(f"Target audiences query: {marketing.target_audiences.all()}")
        print(f"Phone numbers to send SMS to: {to}")



        # Send the SMS
        response = send_sms(to, message)
        return {"status": "success", "response": response}
    except Marketing.DoesNotExist:
        return {"status": "error", "message": "Marketing not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@shared_task
def send_end_marketing_sms(marketing_id):
    """
    Sends an ending SMS for a specific Marketing campaign to its target audiences.
    """
    try:
        print(f"Task started for marketing ID: {marketing_id}")
        marketing = Marketing.objects.get(id=marketing_id)

        # Correctly access related target audiences using the instance
        to = list(marketing.target_audiences.all().values_list('phone_number', flat=True))
        message = f"{marketing.message}\n تنها 2 روز ازین کمپین باقی مانده است"

        # Send the SMS
        response = send_sms(to, message)
        return {"status": "success", "response": response}
    except Marketing.DoesNotExist:
        return {"status": "error", "message": "Marketing not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}