from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Profile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(
            user=instance,
            defaults={'phone_number': instance.phone_number,
            'name': instance.first_name,
            'last_name': instance.last_name,
            }
        )

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        pass
