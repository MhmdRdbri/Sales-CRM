# serializers.py
from rest_framework import serializers
from .models import SalesOpportunity
from products.models import Product

class SalesOpportunitySerializer(serializers.ModelSerializer):
    selected_products = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), many=True
    )

    class Meta:
        model = SalesOpportunity
        fields = [
            'id', 'follow_up_date', 'estimated_amount', 'opportunity_priority',
            'selected_products', 'description', 'created_at', 'profile'
        ]
