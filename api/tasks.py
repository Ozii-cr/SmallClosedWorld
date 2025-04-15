import time
import logging
from celery import shared_task

logger = logging.getLogger(__name__)

@shared_task
def process_request(request_id, email, message):
    """
    Simulates a time-consuming task
    """
   
    logger.info(f"Starting to process request {request_id} for {email}")
    
    #hold process for two minutes
    time.sleep(120)  
    
    result = f"Processed message for {email}: {message}"
    logger.info(f"Completed processing request {request_id}: {result}")
    
    from .models import ProcessRequest
    request = ProcessRequest.objects.get(id=request_id)
    request.status = 'COMPLETED'
    request.result = result
    request.save()
    
    return result