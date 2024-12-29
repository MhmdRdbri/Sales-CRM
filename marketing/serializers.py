from rest_framework import serializers 
from .models import *
from django.utils.timezone import now, make_aware
from datetime import datetime

class MarketingSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Marketing
        fields = '__all__'
        
    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        # Combine date and time
        
        if not start_date.tzinfo:
            start_date = make_aware(start_date)  # Ensure timezone-awareness

        # Check if the date and time are in the past
        if start_date < now():
            raise serializers.ValidationError("Cannot schedule SMS for a past date or time.")
        
        if not end_date.tzinfo:
            end_date = make_aware(end_date)  # Ensure timezone-awareness

        # Check if the date and time are in the past
        if end_date < (now() and start_date):
            raise serializers.ValidationError("Cannot schedule SMS for a past date or time.")
        
        return data        