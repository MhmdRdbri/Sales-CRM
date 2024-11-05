from rest_framework import permissions,viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Product
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status



#create a post and list all products
class ProductListCreateView(APIView):
    serializer_class = ProductSerializer
    permission_classes=[permissions.AllowAny]
    
    def get(self,request:Request,*args, **kwargs):
        
        products = Product.objects.all()
        
        serilizer= self.serializer_class(instance=products,many=True)
        
        return Response(data=serilizer.data,status=status.HTTP_200_OK)
    
    def post(self,request:Request):
        
        data=request.data
        
        serializer=self.serializer_class(data=data)
        
        if serializer.is_valid():
            serializer.save()
            
            response={
                'massage':"product Created Succesfully!",
                'data' : serializer.data
            }
            
            return Response(data=response,status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
 
 
 
 
 #view and update and delete a product by id
class ProductRetrieveUpdateDeleteView(APIView):
    
       serializer_class = ProductSerializer
       permission_classes=[permissions.AllowAny]
       
       def get(self,request=Request,product_id=int):
           product = get_object_or_404(Product,pk=product_id)
           
           serializer=self.serializer_class(instance=product)
           
           return Response(data=serializer.data,status=status.HTTP_200_OK)
       
       
       def put(self,request:Request,product_id=int):
           
            product = get_object_or_404(Product,pk=product_id)
            
            data = request.data
            
            serializer = self.serializer_class(instance=product,data=data)
            
            if serializer.is_valid():
                serializer.save()
                
                response={
                    "message":"product updated",
                    "data" : serializer.data
                }
                return Response(data=response,status=status.HTTP_200_OK)
            
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
        
    
       def delete(self,request:Request,product_id=int):
           product = get_object_or_404(Product,pk=product_id)
           
           product.delete()
           
           return Response(status=status.HTTP_204_NO_CONTENT)
       
       
       def patch(self, request: Request, product_id: int):
            product = get_object_or_404(Product, pk=product_id)
            data = request.data
            serializer = self.serializer_class(instance=product, data=data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                response = {
                    "message": "product partially updated",
                    "data": serializer.data
                }
                return Response(data=response, status=status.HTTP_200_OK)
            
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

       
       
       

class CategoryListCreateView(APIView):
    
    permission_classes=[permissions.AllowAny]
    serializer_class=CategorySerializer
    
    def post(self,request:Request):
        
        data=request.data
        
        serializer=self.serializer_class(data=data)
        
        if serializer.is_valid():
            serializer.save()
            
            response={
                'massage':"category Created Succesfully!",
                'data' : serializer.data
            }
            
            return Response(data=response,status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    
    def get(self,request:Request,*args, **kwargs):
        
        categories = Category.objects.all()
            
        serilizer= self.serializer_class(instance=categories,many=True)
            
        return Response(data=serilizer.data,status=status.HTTP_200_OK)
    
   
   
class CategoryRetrieveUpdateDeleteView(APIView):
    
       serializer_class = CategorySerializer
       permission_classes=[permissions.AllowAny]
       
       def get(self,request=Request,category_id=int):
           category = get_object_or_404(Category,pk=category_id)
           
           serializer=self.serializer_class(instance=category)
           
           return Response(data=serializer.data,status=status.HTTP_200_OK)
       
       
       def put(self,request=Request,category_id=int):
           
            category = get_object_or_404(Category,pk=category_id)
            
            data = request.data
            
            serializer = self.serializer_class(instance=category,data=data)
            
            if serializer.is_valid():
                serializer.save()
                
                response={
                    "message":"category updated",
                    "data" : serializer.data
                }
                return Response(data=response,status=status.HTTP_200_OK)
            
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
            
       
       def delete(self,request=Request,category_id=int):
           product = get_object_or_404(Category,pk=category_id)
           
           product.delete()
           
           return Response(status=status.HTTP_204_NO_CONTENT)
       
       
       
       def patch(self, request: Request, category_id: int):
            product = get_object_or_404(Category, pk=category_id)
            data = request.data
            serializer = self.serializer_class(instance=product, data=data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                response = {
                    "message": "category partially updated",
                    "data": serializer.data
                }
                return Response(data=response, status=status.HTTP_200_OK)
            
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
