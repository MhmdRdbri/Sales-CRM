from celery import shared_task
from ippanel import Client, Error, HTTPError
import logging
from .utils import *
from accountemployee.models import CustomUser

logger = logging.getLogger(__name__)

@shared_task
def send_sales_opportunity_sms(opportunity_id):
    try:
        logger.info(f"Sending SMS for Sales Opportunity ID: {opportunity_id}")
                
        from .models import SalesOpportunity
        
        # Get the opportunity
        opportunity = SalesOpportunity.objects.get(id=opportunity_id)

        # Assume the phone number is stored in the associated customer profile
        users = CustomUser.objects.all()
        phone_numbers = list(users.values_list('phone_number', flat=True))
        message = prepare_sms_message(opportunity)
        
        

        logger.info(f"SMS sent successfully for Sales Opportunity ID: {opportunity.id} - Message ID: {opportunity.sms_task_id}")
        response = send_sms_to_users(phone_numbers,message)
        
        logger.info(phone_numbers)
        logger.debug(f"Response: {response}")
        return {"status": "success", "response": response}
    except SalesOpportunity.DoesNotExist:
        logger.error("oppurtonity not found")
        return {"status": "error", "message": "Notice not found"}
    except Exception as e:
        logger.exception("An error occurred")
        return {"status": "error", "message": str(e)}
