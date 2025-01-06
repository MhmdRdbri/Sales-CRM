from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Factors
from .tasks import update_customer_rank_task

# Trigger rank update when a factor is created or updated
@receiver(post_save, sender=Factors)
def trigger_customer_rank_update(sender, instance, **kwargs):
    if instance.costumer:
        update_customer_rank_task.delay(instance.costumer.id)

# Trigger rank update when a factor is deleted
@receiver(post_delete, sender=Factors)
def trigger_customer_rank_update_on_delete(sender, instance, **kwargs):
    if instance.costumer:
        update_customer_rank_task.delay(instance.costumer.id)
