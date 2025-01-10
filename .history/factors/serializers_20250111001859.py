from rest_framework import serializers
from .models import Factors, FactorItem
from products.models import Product

class FactorProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class FactorSerializer(serializers.ModelSerializer):
    products = FactorProductSerializer(many=True, write_only=True, required=False)
    files = serializers.FileField(write_only=True, required=False)  # Expect a single file

    class Meta:
        model = Factors
        fields = ['id', 'contract_date', 'price', 'description', 'costumer', 'products', 'files']

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