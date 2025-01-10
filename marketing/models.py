from django.db import models
from customerprofile.models import CustomerProfile
from django.utils.timezone import now
from multiselectfield import MultiSelectField


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
    
    TARGET_RANK_CHOICES = CustomerProfile.BUYER_RANK_CHOICES
    
    target_rank = MultiSelectField(
        choices=TARGET_RANK_CHOICES,
        blank=True,
        help_text="Select the target ranks for this campaign."
    )
    
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Assign target audiences based on `target_rank`
        if self.target_rank:
            eligible_profiles = CustomerProfile.objects.filter(buyer_rank__in=self.target_rank)
            self.target_audiences.set(eligible_profiles)
            
            
    def __str__(self):
        return self.campaign_name