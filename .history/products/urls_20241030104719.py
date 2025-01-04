from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'product'


urlpatterns = [
    path('', ProductListCreateView.as_view(),name="products_list"),
    path('<int:product_id>',ProductRetrieveUpdateDeleteView.as_view(),name="products_detail"),
    path("category/",CategoryListCreateView.as_view(),name="category_list"),
    path("category/<int:category_id>",CategoryRetrieveUpdateDeleteView.as_view(),name="category_detail"),
]