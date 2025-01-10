from rest_framework import serializers
from .models import Factors, FactorItem
from products.models import Product
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class FactorProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class FactorSerializer(serializers.ModelSerializer):
    # Fields for product handling
    products = FactorProductSerializer(many=True, write_only=True, required=False)
    # Fields for file handling
    files = serializers.FileField(write_only=True, required=False)

    class Meta:
        model = Factors
        fields = ['id', 'contract_date', 'price', 'description', 'costumer', 'products', 'files']

    def validate_products(self, value):
        """Ensure all product IDs exist."""
        for item in value:
            product_id = item['product_id']
            if not Product.objects.filter(id=product_id).exists():
                raise serializers.ValidationError(f"Product with ID {product_id} does not exist.")
        return value

    def create(self, validated_data):
        # Extract products and file data
        products_data = validated_data.pop('products', [])
        file = validated_data.pop('files', None)

        # Create the factor instance
        factor = Factors.objects.create(**validated_data)

        # Create FactorItem instances for each product
        for item in products_data:
            product = Product.objects.get(id=item['product_id'])
            FactorItem.objects.create(factor=factor, product=product, quantity=item['quantity'])

        # Save the uploaded file if provided
        if file:
            file_path = default_storage.save(f'factor_files/{file.name}', ContentFile(file.read()))
            factor.files = file_path
            factor.save()

        return factor

    def to_representation(self, instance):
        """Customize the serialized output."""
        # Default factor representation
        representation = super().to_representation(instance)

        # Add product details
        representation['products'] = [
            {
                "product_id": item.product.id,
                "quantity": item.quantity
            }
            for item in instance.items.all()  # Use related_name 'items'
        ]

        # Include file URL (if present)
        if instance.files:
            representation['files'] = default_storage.url(instance.files)
        else:
            representation['files'] = None

        return representation