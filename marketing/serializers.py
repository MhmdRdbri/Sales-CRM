from rest_framework import serializers 
from .models import *
from django.utils.timezone import now, make_aware
from datetime import datetime

class MarketingSerializer(serializers.ModelSerializer):
    target_rank = serializers.ListField(
        child=serializers.ChoiceField(choices=CustomerProfile.BUYER_RANK_CHOICES),
        required=True,
    )
    
    
    class Meta:
        model = Marketing
        fields = '__all__'
        
    
    
    def create(self, validated_data):
        # Create the Marketing instance
        marketing_instance = super().create(validated_data)

        # Filter and assign target audiences based on buyer_rank
        target_audiences = CustomerProfile.objects.filter(buyer_rank__in=marketing_instance.target_rank)
        marketing_instance.target_audiences.set(target_audiences)

        return marketing_instance
        
    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        # Combine date and time
        
        if start_date and not start_date.tzinfo:
            start_date = make_aware(start_date)  # Converts naive datetime to timezone-aware
        if end_date and not end_date.tzinfo:
            end_date = make_aware(end_date)

        # Check if the date and time are in the past
        if start_date < now():
            raise serializers.ValidationError("Cannot schedule SMS for a past date or time.")

        # Check if the date and time are in the past
        if end_date < (now() and start_date):
            raise serializers.ValidationError("Cannot schedule SMS for a past date or time.")
        
        data['start_date'] = start_date
        data['end_date'] = end_date
        return data        