from django.db import models
from customerprofile.models import CustomerProfile



class Notice(models.Model):
    title = models.CharField(null=False,blank=False)
    text = models.TextField(null=False,blank=False)
    send_time = models.TimeField(null=False,blank=False)
    send_date = models.DateField(null=False,blank=False)    
    audiences = models.ManyToManyField(CustomerProfile,related_name="notice",blank=True)
    
    def __str__(self):
        return self.title

