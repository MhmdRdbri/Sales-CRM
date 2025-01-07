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


def make_timezone_aware(dt):
    """Helper function to make a datetime timezone-aware if it isn't already."""
    if not dt.tzinfo:
        return make_aware(dt)
    return dt


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

        # Ensure start_date and end_date are timezone-aware
        start_datetime = make_timezone_aware(marketing.start_date)
        end_datetime = make_timezone_aware(marketing.end_date)

        # Calculate two days before end date
        two_days_before_end_date = make_timezone_aware(end_datetime - timedelta(days=2))

        if start_datetime < now():
            raise PermissionDenied("Cannot schedule SMS for a past date or time.")
        if two_days_before_end_date < now():
            raise PermissionDenied("Cannot schedule end SMS for a past date or time.")

        # Assign target audiences based on rank
        # Example: You can change this logic to include/exclude specific ranks
        target_rank = self.request.data.get('target_rank', [])
        if not target_rank:
            raise PermissionDenied("Please specify at least one target rank.")

        eligible_profiles = CustomerProfile.objects.filter(buyer_rank__in=target_rank)
        marketing.target_audiences.set(eligible_profiles)

        # Schedule the SMS tasks and save their task IDs
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
