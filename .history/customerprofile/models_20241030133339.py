from django.db import models


class CustomerProfile(models.Model):
    BRONZE = 'BR'
    SILVER = 'SI'
    GOLD = 'GO'
    
    BUYER_RANK_CHOICES = [
        (BRONZE, 'Bronze'),
        (SILVER, 'Silver'),
        (GOLD, 'Gold'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.BigIntegerField()
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    telegram_id = models.CharField(max_length=255, null=True, blank=True)
    national_id = models.BigIntegerField(null=True, blank=True)
    instagram_id = models.CharField(max_length=255, null=True, blank=True)
    buyer_rank = models.CharField(
        max_length=2,
        choices=BUYER_RANK_CHOICES,
        null=True,
        blank=True
    )
    contracts = models.ForeignKey(
        'contract.Contract',  # Referencing the future model as 'app_name.ModelName'
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.full_name