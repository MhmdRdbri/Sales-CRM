from django.db import models
from customerprofile.models import CustomerProfile
from products.models import Product


class Factors(models.Model):
    contract_date = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()
    description = models.TextField()
    costumer = models.ForeignKey(CustomerProfile, related_name='factor', on_delete=models.SET_NULL,null=True)
    files = models.JSONField(default=list, blank=True)
    
    def __str__(self):
        return f"Factor #{self.id} - {self.contract_date}"
    

class FactorItem(models.Model):
    factor = models.ForeignKey(Factors, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.product_name} - {self.quantity}"
