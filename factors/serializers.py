from rest_framework import serializers
from .models import Factors, FactorItem
from products.models import Product
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import json
from rest_framework.exceptions import ValidationError
import logging
from django.http import QueryDict

logger = logging.getLogger(__name__)

# Serializer for factor items (products in a factor)
class FactorItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name', read_only=True)  # Include product name for clarity

    class Meta:
        model = FactorItem
        fields = ['product', 'product_name', 'quantity']  # Fields to display in GET requests


# Serializer for creating/updating products in a factor
class FactorProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)



class FactorSerializer(serializers.ModelSerializer):
    products = FactorProductSerializer(many=True, write_only=True, required=False)  # For creating/updating
    items = FactorItemSerializer(many=True, read_only=True)  # For reading existing factor items
    files = serializers.FileField(required=False)
  # For including the file path in the response

    class Meta:
        model = Factors
        fields = ['id', 'contract_date', 'price', 'description', 'costumer', 'products', 'items', 'files']

    def get_files(self, obj):
        if obj.files:
            return settings.MEDIA_URL + obj.files.name  # Return the full URL of the file
        return None
    def get_items(self, obj):
        return [
            {"product_id": item.product.id, "product_name": item.product.product_name, "quantity": item.quantity}
            for item in obj.items.all()
        ]
        

    def to_internal_value(self, data):
        if isinstance(data, QueryDict):
            data = data.dict()  # Convert QueryDict to a regular dictionary
        if 'products' in data and isinstance(data['products'], str):
            try:
                products_list = []
                for item in data['products'].split(','):
                    product_id, quantity = item.split(':')
                    products_list.append({
                        'product_id': int(product_id.strip()),
                        'quantity': int(quantity.strip())
                    })
                data['products'] = products_list
            except (ValueError, AttributeError):
                raise serializers.ValidationError({"products": "Invalid format. Expected 'product_id:quantity,product_id:quantity'."})
        return super().to_internal_value(data)



    def create(self, validated_data):
        # Extract and handle `products` field
        products_data = validated_data.pop('products', [])

        # Create the factor instance
        factor = Factors.objects.create(**validated_data)

        # Create FactorItem objects
        for item in products_data:
            try:
                product = Product.objects.get(id=item['product_id'])
                FactorItem.objects.create(factor=factor, product=product, quantity=item['quantity'])
            except Product.DoesNotExist:
                raise serializers.ValidationError({"product_id": f"Product with ID {item['product_id']} does not exist."})

        return factor