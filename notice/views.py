from django.shortcuts import render
from rest_framework import generics
from .models import Notice
from .serializers import NoticeSerializer
from rest_framework.permissions import *
from rest_framework.exceptions import PermissionDenied
from datetime import datetime
from .tasks import send_notice_sms
from django.utils.timezone import make_aware , now, timezone
from celery import current_app







class NoticeList(generics.ListCreateAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [IsAuthenticated]
    
    

    def get(self, request, *args, **kwargs):      
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.request.user.profile.work_position != 'system_manager' and self.request.user.profile.work_position != 'admin':
            raise PermissionDenied("You do not have permission post any notice.")
        
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        notice = serializer.save()

        # Combine date and time
        send_datetime = datetime.combine(notice.send_date, notice.send_time)
        if not send_datetime.tzinfo:
            send_datetime = make_aware(send_datetime)

        if send_datetime < now():
            raise PermissionDenied("Cannot schedule SMS for a past date or time.")

        # Schedule the SMS task and save the task ID
        task = send_notice_sms.apply_async((notice.id,), eta=send_datetime)
        notice.task_id = task.id
        notice.save()  # Save the task ID in the database





class NoticeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    
    def put(self, request, *args, **kwargs):
        notice = self.get_object()

        # Permission check
        if self.request.user.profile.work_position not in ['system_manager', 'admin']:
            raise PermissionDenied("You do not have permission to update this notice.")

        # Revoke the old task if it exists
        if notice.task_id:
            current_app.control.revoke(notice.task_id, terminate=True)
            print(f"Revoked old task with ID: {notice.task_id}")

        # Combine date and time to form send_datetime
        send_datetime = datetime.combine(notice.send_date, notice.send_time)

        # Make sure send_datetime is timezone-aware in UTC
        if not send_datetime.tzinfo:
            send_datetime = make_aware(send_datetime, timezone=timezone.utc)  # Use timezone.utc here

        # Get the current time in UTC
        current_time = now()  # This will be in UTC if your settings use USE_TZ=True

        # Compare the times in UTC
        if send_datetime < current_time:
            raise PermissionDenied("Cannot schedule SMS for a past date or time.")

        # Update the notice and schedule a new task
        response = self.update(request, *args, **kwargs)

        task = send_notice_sms.apply_async((notice.id,), eta=send_datetime)
        notice.task_id = task.id
        notice.save()

        print(f"Scheduled new task with ID: {task.id} for notice ID: {notice.id}")
        return response
    
    
    def delete(self, request, *args, **kwargs):
        notice = self.get_object()

        # Permission check
        if self.request.user.profile.work_position not in ['system_manager', 'admin']:
            raise PermissionDenied("You do not have permission to delete this notice.")

        # Revoke the task if it exists
        if notice.task_id:
            current_app.control.revoke(notice.task_id, terminate=True)
            print(f"Revoked task with ID: {notice.task_id}")

        return self.destroy(request, *args, **kwargs)
