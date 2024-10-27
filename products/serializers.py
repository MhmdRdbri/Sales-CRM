from rest_framework import serializers
from .models import Product


class ProductSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields= ['id','product_name','price','status','size','color','product_image','description']