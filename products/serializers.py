from rest_framework import serializers
from .models import Product,Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields= ['id','product_name','price','status','size','color','product_image','description','category','brand']
        
        
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','category_name']
        
        