from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Factors

from .tasks import update_customer_rank_task

@receiver(post_save, sender=Factors)
def trigger_customer_rank_update(sender, instance, **kwargs):
    if instance.costumer:
        update_customer_rank_task.delay(instance.costumer.id)
