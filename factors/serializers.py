
from rest_framework import serializers
from .models import Factors
from products.models import Product
from products.serializers import ProductSerilizer

class FactorProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class FactorSerializer(serializers.ModelSerializer):
    products = FactorProductSerializer(many=True)

    class Meta:
        model = Factors
        fields = '__all__'

    def validate_products(self, value):
        for item in value:
            product_id = item['product_id']
            if not Product.objects.filter(id=product_id).exists():
                raise serializers.ValidationError(f"Product with ID {product_id} does not exist.")
        return value

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        factor = Factors.objects.create(**validated_data)
        factor.products = products_data
        factor.save()
        return factor

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        products_detailed = []
        
        for item in instance.products:
            try:
                product = Product.objects.get(id=item['product_id'])
                products_detailed.append({
                    "product": ProductSerilizer(product).data,
                    "quantity": item['quantity'],
                    "total_price": item['quantity'] * product.price
                })
            except Product.DoesNotExist:
                continue

        representation['products'] = products_detailed
        representation['total_cost'] = instance.total_cost()
        return representation
