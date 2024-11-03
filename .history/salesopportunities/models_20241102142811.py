from django.db import models
from django.conf import settings
from products.models import *

class SalesOpportunity(models.Model):
    follow_up_date = models.DateField()
    estimated_amount = models.BigIntegerField()
    
    OPPORTUNITY_PRIORITY_CHOICES = [
        ('low_priority', 'low_priority'),
        ('mid_priority', 'mid_priority'),
        ('high_priority', 'high_priority'),
    ]
    opportunity_priority = models.CharField(max_length=10, choices=OPPORTUNITY_PRIORITY_CHOICES)
    
    selected_products = models.ManyToManyField(Product, related_name='sales_opportunities')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='sales_opportunities')

    def __str__(self):
        return f"Opportunity {self.id} - Priority: {self.opportunity_priority}"
