from django.db import models
from django.utils import timezone


class CustomerProfile(models.Model):
    BRONZE = 'BR'
    SILVER = 'SI'
    GOLD = 'GO'

    BUYER_RANK_CHOICES = [
        (BRONZE, 'Bronze'),
        (SILVER, 'Silver'),
        (GOLD, 'Gold'),
    ]


    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    telegram_id = models.CharField(max_length=255, null=True, blank=True)
    national_id = models.BigIntegerField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    instagram_id = models.CharField(max_length=255, null=True, blank=True)
    buyer_rank = models.CharField(
        max_length=2,
        choices=BUYER_RANK_CHOICES,
        default=BRONZE,
        blank=True
    )

    customer_picture = models.ImageField(upload_to='customer_profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.full_name