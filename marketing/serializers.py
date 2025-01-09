from rest_framework import serializers 
from .models import *
from django.utils.timezone import now, make_aware
from datetime import datetime

class MarketingSerializer(serializers.ModelSerializer):
    target_rank = serializers.ListField(
        child=serializers.ChoiceField(choices=CustomerProfile.BUYER_RANK_CHOICES),
        write_only=True,
        required=True,
    )
    
    
    class Meta:
        model = Marketing
        fields = '__all__'
        
    
    
    def create(self, validated_data):
        # Extract target_rank from validated data
        target_rank = validated_data.pop('target_rank', [])
        
        # Create the Marketing instance
        marketing_instance = super().create(validated_data)
        
        # Filter and assign target audiences based on rank
        target_audiences = CustomerProfile.objects.filter(rank__in=target_rank)
        marketing_instance.target_audiences.set(target_audiences)
        
        return marketing_instance
        
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