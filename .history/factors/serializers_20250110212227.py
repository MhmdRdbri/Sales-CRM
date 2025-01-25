from rest_framework import serializers
from .models import Factors, FactorItem
from products.models import Product
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class FactorProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class FactorSerializer(serializers.ModelSerializer):
    products = FactorProductSerializer(many=True, write_only=True, required=False)
    files = serializers.FileField(write_only=True, required=False)

    class Meta:
        model = Factors
        fields = ['id', 'contract_date', 'price', 'description', 'costumer', 'products', 'files']

    def create(self, validated_data):
        # Extract products and file data
        products_data = validated_data.pop('products', [])
        file = validated_data.pop('files', None)

        # Debug: Ensure products_data is being processed
        print("Products Data:", products_data)

        # Create factor instance
        factor = Factors.objects.create(**validated_data)

        # Debug: Verify factor instance creation
        print("Factor Created:", factor)

        # Create FactorItem instances
        for item in products_data:
            product = Product.objects.get(id=item['product_id'])
            FactorItem.objects.create(factor=factor, product=product, quantity=item['quantity'])
            print(f"FactorItem Created for Product ID {product.id} with Quantity {item['quantity']}")

        # Handle file upload if provided
        if file:
            file_path = default_storage.save(f'factor_files/{file.name}', ContentFile(file.read()))
            factor.files = file_path

        factor.save()
        return factor

    def to_representation(self, instance):
        # Get default representation
        representation = super().to_representation(instance)

        # Include products in the response
        representation['products'] = [
            {
                "product_id": item.product.id,
                "quantity": item.quantity
            }
            for item in instance.items.all()
        ]

        # Add file URL to representation
        representation['files'] = default_storage.url(instance.files) if instance.files else None

        return representation
