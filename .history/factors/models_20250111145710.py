from django.db import models
from customerprofile.models import CustomerProfile
from products.models import Product


class Factor(models.Model):
    contract_date = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    customer = models.ForeignKey(
        CustomerProfile, related_name='factors', on_delete=models.SET_NULL, null=True
    )
    file = models.FileField(upload_to='factor_files/', blank=True, null=True)

    def __str__(self):
        return f"Factor #{self.id} - {self.contract_date}"


class FactorItem(models.Model):
    factor = models.ForeignKey(
        Factor, related_name='items', on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.product_name} - {self.quantity}"
