from django.db import models
from django.conf import settings

class SalesOpportunity(models.Model):
    id = models.BigAutoField(primary_key=True)
    follow_up_date = models.DateField()
    estimated_amount = models.BigIntegerField()
    
    OPPORTUNITY_PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    opportunity_priority = models.CharField(max_length=10, choices=OPPORTUNITY_PRIORITY_CHOICES)
    
    selected_product = models.BigIntegerField()  # Assume this relates to a Product model
    description = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    
    # Assuming 'profile' is a foreign key to a Profile model
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='sales_opportunities')

    def __str__(self):
        return f"Opportunity {self.id} - Priority: {self.opportunity_priority}"
