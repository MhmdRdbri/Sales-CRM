# serializers.py
from rest_framework import serializers
from .models import SalesOpportunity
from products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'price']

class SalesOpportunitySerializer(serializers.ModelSerializer):
    selected_products = ProductSerializer(many=True)

    class Meta:
        model = SalesOpportunity
        fields = ['id', 'follow_up_date', 'estimated_amount', 'opportunity_priority',
                  'selected_products', 'description', 'created_at', 'profile']

    def create(self, validated_data):
        products_data = validated_data.pop('selected_products')
        sales_opportunity = SalesOpportunity.objects.create(**validated_data)
        for product_data in products_data:
            sales_opportunity.selected_products.add(product_data['id'])
        return sales_opportunity

    def update(self, instance, validated_data):
        products_data = validated_data.pop('selected_products', None)
        instance.follow_up_date = validated_data.get('follow_up_date', instance.follow_up_date)
        instance.estimated_amount = validated_data.get('estimated_amount', instance.estimated_amount)
        instance.opportunity_priority = validated_data.get('opportunity_priority', instance.opportunity_priority)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        if products_data is not None:
            instance.selected_products.clear()
            for product_data in products_data:
                instance.selected_products.add(product_data['id'])
        return instance
