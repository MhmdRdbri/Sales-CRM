from rest_framework import viewsets
from rest_framework.exceptions import ValidationError,PermissionDenied
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.utils.timezone import make_aware,now
from datetime import datetime, timedelta, time
from celery import current_app
from .models import SalesOpportunity
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import SalesOpportunitySerializer
from .tasks import send_sales_opportunity_sms

class SalesOpportunityViewSet(viewsets.ModelViewSet):
    queryset = SalesOpportunity.objects.all()
    serializer_class = SalesOpportunitySerializer

    def perform_create(self, serializer):
        opportunity = serializer.save()

        # Set the send time to 8 AM on the follow_up_date
        follow_up_date = opportunity.follow_up_date
        send_datetime = datetime.combine(follow_up_date, time(8, 0))  # Set time to 8 AM

        # Ensure send_datetime is timezone-aware
        if not send_datetime.tzinfo:
            send_datetime = make_aware(send_datetime)  # Make it timezone-aware

        # Check if the send datetime is in the past
        if send_datetime < now():
            raise PermissionDenied("Cannot schedule SMS for a past date or time.")

        # Schedule the SMS task and save the task ID
        task = send_sales_opportunity_sms.apply_async((opportunity.id,), eta=send_datetime)
        opportunity.sms_task_id = task.id
        opportunity.save()  # Save the task ID in the database
        
        
    def put(self, request, *args, **kwargs):
        opportunity = self.get_object()



        # Revoke the old task if it exists
        if opportunity.sms_task_id:
            current_app.control.revoke(opportunity.task_id, terminate=True)
            print(f"Revoked old task with ID: {opportunity.task_id}")

        follow_up_date = opportunity.follow_up_date
        send_datetime = datetime.combine(follow_up_date, time(19, 6))  # Set time to 8 AM

        # Ensure send_datetime is timezone-aware
        if not send_datetime.tzinfo:
            send_datetime = make_aware(send_datetime)  # Make it timezone-aware

        # Check if the send datetime is in the past
        if send_datetime < now():
            raise PermissionDenied("Cannot schedule SMS for a past date or time.")

        response = self.update(request, *args, **kwargs)


        # Schedule the SMS task and save the task ID
        task = send_sales_opportunity_sms.apply_async((opportunity.id,), eta=send_datetime)
        opportunity.sms_task_id = task.id
        opportunity.save()  # Save the task ID in the database

        print(f"Scheduled new task with ID: {task.id} for opportunity ID: {opportunity.id}")
        return response
        
        
    def delete(self, request, *args, **kwargs):
        opportunity = self.get_object()
        
        # Revoke the task if it exists
        if opportunity.task_id:
            current_app.control.revoke(opportunity.task_id, terminate=True)
            print(f"Revoked task with ID: {opportunity.task_id}")

        return self.destroy(request, *args, **kwargs)
            
        