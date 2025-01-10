from celery import shared_task
from .utils import send_sms
from .models import Notice
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_notice_sms(notice_id):
    try:
        logger.info(f"Task started for Notice ID: {notice_id}")
        notice = Notice.objects.get(id=notice_id)
        to = list(notice.audiences.values_list('phone_number', flat=True))
        message = notice.text

        response = send_sms(to, message)
        logger.info("SMS sent successfully.")
        logger.debug(f"Response: {response}")
        return {"status": "success", "response": response}
    except Notice.DoesNotExist:
        logger.error("Notice not found")
        return {"status": "error", "message": "Notice not found"}
    except Exception as e:
        logger.exception("An error occurred")
        return {"status": "error", "message": str(e)}
