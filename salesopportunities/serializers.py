from rest_framework import serializers
from .models import SalesOpportunity, SalesOpportunityItem
from products.models import Product


class SalesOpportunityItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOpportunityItem
        fields = ['id', 'product', 'quantity']


class SalesOpportunitySerializer(serializers.ModelSerializer):
    items = SalesOpportunityItemSerializer(many=True, read_only=True)
    new_items = SalesOpportunityItemSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = SalesOpportunity
        fields = [
            'id', 'follow_up_date', 'estimated_amount', 'opportunity_priority','buyer_type',
            'description', 'created_at', 'profile', 'items', 'new_items'
        ]

    def create(self, validated_data):
        new_items_data = validated_data.pop('new_items', [])
        sales_opportunity = SalesOpportunity.objects.create(**validated_data)
        for item_data in new_items_data:
            SalesOpportunityItem.objects.create(sales_opportunity=sales_opportunity, **item_data)
        return sales_opportunity

    def update(self, instance, validated_data):
        new_items_data = validated_data.pop('new_items', [])
        instance = super().update(instance, validated_data)

        # Optionally clear old items
        SalesOpportunityItem.objects.filter(sales_opportunity=instance).delete()

        for item_data in new_items_data:
            SalesOpportunityItem.objects.create(sales_opportunity=instance, **item_data)
        return instance
