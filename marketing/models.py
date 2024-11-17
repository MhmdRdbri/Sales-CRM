from django.db import models
from customerprofile.models import CustomerProfile



class Marketing(models.Model):
    campaign_name = models.CharField(null=False,blank=False)
    start_date = models.DateTimeField(null=False,blank=False)
    end_date = models.DateTimeField(null=False,blank=False)
    message = models.TextField(null=False,blank=False)
    target_audiences = models.ManyToManyField(CustomerProfile,related_name="marketing",blank=True)
    
    def __str__(self):
        return self.campaign_name