from celery import shared_task
from django.db.models import Avg, Sum
from .models import CustomerProfile, Factors

@shared_task
def update_customer_rank_task(customer_id):
    customer = CustomerProfile.objects.get(id=customer_id)
    global_avg = Factors.objects.filter(costumer__factor__isnull=False) \
        .aggregate(avg_price=Avg('price'))['avg_price'] or 0

    customer_spent = customer.factor.aggregate(total_spent=Sum('price'))['total_spent'] or 0

    if customer_spent > global_avg:
        new_rank = CustomerProfile.GOLD
    elif customer_spent < global_avg:
        new_rank = CustomerProfile.SILVER
    else:
        new_rank = CustomerProfile.BRONZE

    if customer.buyer_rank != new_rank:
        customer.buyer_rank = new_rank
        customer.save()
