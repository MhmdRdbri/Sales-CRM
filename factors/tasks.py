from celery import shared_task
from django.db.models import Avg, Sum
from .models import CustomerProfile, Factors

@shared_task
def update_customer_rank_task(customer_id):
    try:
        customer = CustomerProfile.objects.get(id=customer_id)

        # Calculate the global average price
        global_avg = Factors.objects.aggregate(avg_price=Avg('price'))['avg_price'] or 0

        # Calculate the total amount spent by this customer
        customer_spent = customer.factor.aggregate(total_spent=Sum('price'))['total_spent'] or 0

        # Determine new rank based on total spent compared to global average
        if customer_spent > global_avg:
            new_rank = CustomerProfile.GOLD
        elif customer_spent < global_avg:
            new_rank = CustomerProfile.SILVER
        else:
            new_rank = CustomerProfile.BRONZE

        # Update rank only if it has changed
        if customer.buyer_rank != new_rank:
            customer.buyer_rank = new_rank
            customer.save()
    except CustomerProfile.DoesNotExist:
        pass  # Handle cases where the customer profile no longer exists
