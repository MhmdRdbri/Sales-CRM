from rest_framework import serializers
from .models import Factors, FactorItem
from products.models import Product
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

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


# Main serializer for Factors
class FactorSerializer(serializers.ModelSerializer):
    products = FactorProductSerializer(many=True, write_only=True, required=False)  # For creating/updating
    items = FactorItemSerializer(many=True, read_only=True)  # For reading existing factor items
    files = serializers.FileField(write_only=True, required=False)  # File upload support

    class Meta:
        model = Factors
        fields = ['id', 'contract_date', 'price', 'description', 'costumer', 'products', 'items', 'files']

    def create(self, validated_data):
        products_data = validated_data.pop('products', [])  # Extract products data
        file = validated_data.pop('files', None)  # Extract file data

        # Create the factor instance
        factor = Factors.objects.create(**validated_data)

        # Handle related products (FactorItem)
        for item in products_data:
            product = Product.objects.get(id=item['product_id'])
            FactorItem.objects.create(factor=factor, product=product, quantity=item['quantity'])

        # Save the uploaded file if provided
        if file:
            file_path = default_storage.save(f'factor_files/{file.name}', ContentFile(file.read()))
            factor.files = file_path

        factor.save()
        return factor
