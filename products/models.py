from django.db import models

class Category(models.Model):
    category_name=models.CharField(max_length=150)
    
    def __str__(self):
        return self.category_name

    
    
class Product(models.Model):
    product_name = models.CharField(max_length=150)
    price = models.IntegerField()
    status = models.BooleanField(default=False,)
    size = models.CharField()
    color = models.CharField()
    brand = models.CharField()
    product_image = models.ImageField(upload_to='product_image/', null=True, blank=True)
    description = models.TextField()
    category = models.ManyToManyField(Category,related_name="categories",blank=True)
    
    
    
    def __str__(self):
        return self.product_name


