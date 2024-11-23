from rest_framework import serializers
from django.utils.timezone import now, make_aware
from datetime import datetime
from .models import Notice

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'

    def validate(self, data):
        send_date = data.get('send_date')
        send_time = data.get('send_time')

        # Combine date and time
        send_datetime = datetime.combine(send_date, send_time)
        if not send_datetime.tzinfo:
            send_datetime = make_aware(send_datetime)  # Ensure timezone-awareness

        # Check if the date and time are in the past
        if send_datetime < now():
            raise serializers.ValidationError("Cannot schedule SMS for a past date or time.")

        return data
