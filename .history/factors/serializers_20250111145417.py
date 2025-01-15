from rest_framework import serializers
from .models import Factors, FactorItem
from products.models import Product
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.db import transaction

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
    file_url = serializers.SerializerMethodField()  # For including the file URL in the response

    class Meta:
        model = Factors
        fields = ['id', 'contract_date', 'price', 'description', 'costumer', 'products', 'items', 'file_url']

    def get_file_url(self, obj):
        if obj.files and obj.files.name:
            return settings.MEDIA_URL + obj.files.name
        return None

    def create(self, validated_data):
        print("Validated Data:", validated_data)
        products_data = validated_data.pop('products', [])
        file = validated_data.pop('files', None)

        with transaction.atomic():
            factor = Factors.objects.create(**validated_data)

            # Debug: Log created factor
            print(f"Factor created: {factor}")

            # Create related FactorItems
            for item in products_data:
                product = Product.objects.get(id=item['product_id'])
                factor_item = FactorItem.objects.create(factor=factor, product=product, quantity=item['quantity'])
                
                # Debug: Log created factor item
                print(f"FactorItem created: {factor_item}")

            # Save the uploaded file if provided
            if file:
                factor.files.save(file.name, file)
                print(f"File saved: {factor.files.name}")

            factor.save()
        return factor


    def update(self, instance, validated_data):
        products_data = validated_data.pop('products', [])  # Extract products data
        file = validated_data.pop('files', None)  # Extract file data

        # Update factor fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Handle related products (FactorItem)
        if products_data:
            instance.items.all().delete()  # Delete existing items
            for item in products_data:
                product = Product.objects.get(id=item['product_id'])
                FactorItem.objects.create(factor=instance, product=product, quantity=item['quantity'])

        # Update the uploaded file if provided
        if file:
            instance.files.save(file.name, file)

        instance.save()
        return instance
