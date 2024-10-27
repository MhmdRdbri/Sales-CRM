from django.db import models


class Product(models.Model):
    product_name = models.CharField(max_length=150)
    price = models.IntegerField()
    status = models.BooleanField()
    size = models.CharField()
    color = models.CharField()
    product_image = models.CharField()
    description = models.TextField()
    #category = models.ManyToManyField()
    
    
    
    def __str__(self):
        return self.project_name
