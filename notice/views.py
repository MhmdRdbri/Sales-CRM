from django.shortcuts import render
from rest_framework import generics
from .models import Notice
from .serializers import NoticeSerializer
from rest_framework.permissions import *
from rest_framework.exceptions import PermissionDenied
from datetime import datetime
from .tasks import send_notice_sms
from django.utils.timezone import make_aware , now
from datetime import datetime




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
        print("Perform_create method triggered")  # Debug statement
        notice = serializer.save()
        print(f"Notice created with ID: {notice.id}")  # Debug statement

        # Combine date and time
        send_datetime = datetime.combine(notice.send_date, notice.send_time)
        if not send_datetime.tzinfo:
            send_datetime = make_aware(send_datetime)  # Ensure timezone-awareness

        # Get current time in UTC
        current_time = now()  # Django's timezone-aware now()

        print(f"send_datetime: {send_datetime}, current_time: {current_time}")  # Debug statement

        # Check if the send time is in the past
        if send_datetime < current_time:
            print("Invalid send_datetime: Task cannot be scheduled in the past.")  # Debug statement
            raise PermissionDenied("Cannot schedule SMS for a past date or time.")

        # Schedule the SMS task with Celery
        task = send_notice_sms.apply_async((notice.id,), eta=send_datetime)
        print(f"Task scheduled with ID: {task.id} at {send_datetime}")




class NoticeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        notice = self.get_object()
        send_datetime = datetime.combine(notice.send_date, notice.send_time)
        
        if now() > send_datetime:
            raise PermissionDenied("You cannot modify a notice that has already been sent.")
        
        if self.request.user.profile.work_position != 'system_manager' and self.request.user.profile.work_position != 'admin':
            raise PermissionDenied("You do not have permission put change this notice.")
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if self.request.user.profile.work_position != 'system_manager' and self.request.user.profile.work_position != 'admin':
            raise PermissionDenied("You do not have permission delete this  notice.")
        
        return self.destroy(request, *args, **kwargs)

