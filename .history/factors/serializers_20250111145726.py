from rest_framework import serializers
from .models import Factor, FactorItem
from products.models import Product


class FactorItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name', read_only=True)

    class Meta:
        model = FactorItem
        fields = ['product', 'product_name', 'quantity']

class FactorSerializer(serializers.ModelSerializer):
    items = FactorItemSerializer(many=True, read_only=True)  # For GET
    products = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField()
        ),
        write_only=True,
        required=False
    )  # For POST
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Factor
        fields = [
            'id',
            'contract_date',
            'price',
            'description',
            'customer',
            'items',
            'products',
            'file_url'
        ]

    def get_file_url(self, obj):
        if obj.file:
            return obj.file.url
        return None

    def create(self, validated_data):
        products_data = validated_data.pop('products', [])
        file = validated_data.pop('file', None)

        # Create the Factor instance
        factor = Factor.objects.create(**validated_data)

        # Create related FactorItems
        for product_data in products_data:
            product = Product.objects.get(id=product_data['product'])
            FactorItem.objects.create(
                factor=factor,
                product=product,
                quantity=product_data['quantity']
            )

        # Save the file if provided
        if file:
            factor.file.save(file.name, file)

        return factor
