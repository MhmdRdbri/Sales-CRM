from django.db import models
from products.models import Product
from customerprofile.models import CustomerProfile


class SalesOpportunity(models.Model):
    follow_up_date = models.DateField()
    estimated_amount = models.BigIntegerField()
        
    OMDE = 'OM'
    KHORDE= 'KH'
    

    OPPORTUNITY_PRIORITY_CHOICES = [
        ('low_priority', 'low_priority'),
        ('mid_priority', 'mid_priority'),
        ('high_priority', 'high_priority'),
    ]
    BUYER_TYPE_CHOICES = [
        (OMDE, 'Omde'),
        (KHORDE, 'Khorde'),
    ]
    opportunity_priority = models.CharField(max_length=255, choices=OPPORTUNITY_PRIORITY_CHOICES)
    buyer_type = models.CharField(
        max_length=2,
        choices=BUYER_TYPE_CHOICES,
        null=True,
        blank=True
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    profile = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='sales_opportunities')

    def __str__(self):
        return f"Opportunity {self.id} - Priority: {self.opportunity_priority}"


class SalesOpportunityItem(models.Model):
    sales_opportunity = models.ForeignKey(SalesOpportunity, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.product_name} - {self.quantity} (Opportunity {self.sales_opportunity.id})"
