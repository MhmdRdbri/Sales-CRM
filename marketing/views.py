from django.shortcuts import render
from rest_framework import generics
from .models import Marketing
from .serializers import MarketingSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.utils.timezone import make_aware, now
from datetime import timedelta
from .tasks import send_marketing_sms, send_end_marketing_sms
from celery import current_app
from django.utils.timezone import now
from datetime import timedelta
from customerprofile.models import CustomerProfile




class MarketingList(generics.ListCreateAPIView):
    queryset = Marketing.objects.all()
    serializer_class = MarketingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if self.request.user.profile.work_position not in ['system_manager', 'admin']:
            raise PermissionDenied("You do not have permission to post a marketing campaign.")
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        marketing = serializer.save()

        # Ensure start_date and end_date are valid
        start_datetime = marketing.start_date
        end_datetime = marketing.end_date
        two_days_before_end_date = end_datetime - timedelta(days=2)

        if start_datetime < now():
            raise PermissionDenied("Cannot schedule SMS for a past date or time.")
        if two_days_before_end_date < now():
            raise PermissionDenied("Cannot schedule end SMS for a past date or time.")

        # Schedule Celery tasks
        task_start = send_marketing_sms.apply_async((marketing.id,), eta=start_datetime)
        task_end = send_end_marketing_sms.apply_async((marketing.id,), eta=two_days_before_end_date)

        marketing.task_start_id = task_start.id
        marketing.task_end_id = task_end.id
        marketing.save()

class MarketingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Marketing.objects.all()
    serializer_class = MarketingSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        marketing = self.get_object()

        if request.user.profile.work_position not in ['system_manager', 'admin']:
            raise PermissionDenied("You do not have permission to update this marketing campaign.")

        # Revoke old tasks
        if marketing.task_start_id:
            current_app.control.revoke(marketing.task_start_id, terminate=True)
        if marketing.task_end_id:
            current_app.control.revoke(marketing.task_end_id, terminate=True)

        # Update tasks
        send_datetime = make_timezone_aware(marketing.start_date)
        two_days_before_end_date = make_timezone_aware(marketing.end_date - timedelta(days=2))

        if send_datetime < now():
            raise PermissionDenied("Cannot schedule SMS for a past date or time.")
        if two_days_before_end_date < now():
            raise PermissionDenied("Cannot schedule end SMS for a past date or time.")

        task_start = send_marketing_sms.apply_async((marketing.id,), eta=send_datetime)
        task_end = send_end_marketing_sms.apply_async((marketing.id,), eta=two_days_before_end_date)
        marketing.task_start_id = task_start.id
        marketing.task_end_id = task_end.id
        marketing.save()

        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        marketing = self.get_object()

        if request.user.profile.work_position not in ['system_manager', 'admin']:
            raise PermissionDenied("You do not have permission to delete this marketing campaign.")

        # Revoke tasks
        if marketing.task_start_id:
            current_app.control.revoke(marketing.task_start_id, terminate=True)
        if marketing.task_end_id:
            current_app.control.revoke(marketing.task_end_id, terminate=True)

        return self.destroy(request, *args, **kwargs)
