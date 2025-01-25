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
    files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Factors
        fields = ['id', 'contract_date', 'price', 'description', 'costumer', 'products', 'files']

    def validate_products(self, value):
        # Ensure that each product_id exists
        for item in value:
            product_id = item['product_id']
            if not Product.objects.filter(id=product_id).exists():
                raise serializers.ValidationError(f"Product with ID {product_id} does not exist.")
        return value

    def create(self, validated_data):
        products_data = validated_data.pop('products', [])
        file = validated_data.pop('files', None)

        # Create the factor instance
        factor = Factors.objects.create(**validated_data)

        # Handle products
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
        # Get the default representation for the factor
        representation = super().to_representation(instance)

        # Add products with only product_id and quantity from FactorItem
        representation['products'] = [
            {
                "product_id": item.product.id,
                "quantity": item.quantity
            }
            for item in instance.items.all()  # Use related_name 'items' to access FactorItems
        ]

        # Add full URLs for files in the representation
        representation['files'] = [default_storage.url(path) for path in instance.files]

        return representation
