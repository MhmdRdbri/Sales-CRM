from django.db import models
from customerprofile.models import CustomerProfile
from django.utils.timezone import now


class Marketing(models.Model):
    campaign_name = models.CharField(null=False,blank=False)
    start_date = models.DateTimeField(null=False,blank=False)
    end_date = models.DateTimeField(null=False,blank=False)
    message = models.TextField(null=False,blank=False)
    target_audiences = models.ManyToManyField(CustomerProfile,related_name="marketing",blank=True)
    task_start_id = models.CharField(max_length=255, null=True, blank=True)
    task_end_id = models.CharField(max_length=255, null=True, blank=True)
    STATUS_CHOICES = [
        ('undone', 'Undone'),
        ('working', 'Working'),
        ('done', 'Done'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='undone')
    
    def __str__(self):
        return self.campaign_name