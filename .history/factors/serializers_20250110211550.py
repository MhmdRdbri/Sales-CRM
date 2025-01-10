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

    def validate_products(self, value):
        for item in value:
            product_id = item['product_id']
            if not Product.objects.filter(id=product_id).exists():
                raise serializers.ValidationError(f"Product with ID {product_id} does not exist.")
        return value

    def create(self, validated_data):
        # Extract products and file data
        products_data = validated_data.pop('products', [])
        file = validated_data.pop('files', None)

        # Log the validated data for debugging
        print("Validated data:", validated_data)
        print("Products data:", products_data)

        # Create the factor instance
        factor = Factors.objects.create(**validated_data)

        # Handle products
        for item in products_data:
            product = Product.objects.get(id=item['product_id'])
            FactorItem.objects.create(factor=factor, product=product, quantity=item['quantity'])

        # Handle file upload
        if file:
            file_path = default_storage.save(f'factor_files/{file.name}', ContentFile(file.read()))
            factor.files = file_path
            factor.save()

        return factor

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Add products
        representation['products'] = [
            {"product_id": item.product.id, "quantity": item.quantity}
            for item in instance.items.all()
        ]
        # Add file URL
        if instance.files:
            representation['files'] = default_storage.url(instance.files)
        else:
            representation['files'] = None
        return representation