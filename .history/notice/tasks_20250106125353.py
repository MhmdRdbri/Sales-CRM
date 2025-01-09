from celery import shared_task
from .utils import send_sms
from .models import Notice

@shared_task(queue='sms_queue')
def send_notice_sms(notice_id):
    """
    Sends SMS for a specific Notice to its audiences.
    
    Args:
        notice_id (int): The ID of the Notice to send.
    """
    try:
        
        print(f"Task started for Notice ID: {notice_id}")
        notice = Notice.objects.get(id=notice_id)
        # Get phone numbers from the related CustomerProfile objects
        to = list(notice.audiences.values_list('phone_number', flat=True))
        message = notice.text

        # Send the SMS
        response = send_sms(to, message)
        return {"status": "success", "response": response}
    except Notice.DoesNotExist:
        return {"status": "error", "message": "Notice not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
