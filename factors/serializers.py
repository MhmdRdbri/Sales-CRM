from rest_framework import serializers
from .models import Factors, FactorItem
from products.models import Product

class FactorProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class FactorSerializer(serializers.ModelSerializer):
    # products field to handle product_id and quantity
    products = FactorProductSerializer(many=True, write_only=True)

    class Meta:
        model = Factors
        fields = ['id', 'contract_date', 'price', 'description', 'costumer', 'products']

    def validate_products(self, value):
        # Ensure that each product_id exists
        for item in value:
            product_id = item['product_id']
            if not Product.objects.filter(id=product_id).exists():
                raise serializers.ValidationError(f"Product with ID {product_id} does not exist.")
        return value

    def create(self, validated_data):
        # Remove products data from validated_data
        products_data = validated_data.pop('products')
        # Create the factor instance
        factor = Factors.objects.create(**validated_data)

        # Create a FactorItem for each product in the products data
        for item in products_data:
            product = Product.objects.get(id=item['product_id'])
            FactorItem.objects.create(factor=factor, product=product, quantity=item['quantity'])

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
        
        return representation
