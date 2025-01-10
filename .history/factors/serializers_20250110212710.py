from rest_framework import serializers
from .models import Factors, FactorItem
from products.models import Product


class FactorItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactorItem
        fields = ['product', 'quantity']


class FactorSerializer(serializers.ModelSerializer):
    items = FactorItemSerializer(many=True, write_only=True)  # Nested input for FactorItem

    class Meta:
        model = Factors
        fields = ['id', 'contract_date', 'price', 'description', 'costumer', 'files', 'items']

    def create(self, validated_data):
        # Extract nested FactorItem data
        items_data = validated_data.pop('items', [])

        # Create the Factors instance
        factor = Factors.objects.create(**validated_data)

        # Create associated FactorItem instances
        for item_data in items_data:
            FactorItem.objects.create(factor=factor, **item_data)

        return factor

    def to_representation(self, instance):
        # Get the default representation for the factor
        representation = super().to_representation(instance)

        # Include related FactorItem data in the output
        representation['items'] = [
            {
                "product": item.product.id,
                "quantity": item.quantity
            }
            for item in instance.items.all()  # Use related_name 'items'
        ]
        return representation
