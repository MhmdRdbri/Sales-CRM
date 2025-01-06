from rest_framework import generics
from .models import CustomerProfile
from .serializers import *
from rest_framework.permissions import *
from rest_framework.exceptions import PermissionDenied
from factors.models import Factors
from django.db.models import Avg, Sum

class CustomerProfileListCreateView(generics.ListCreateAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]

class CustomerProfileRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]


    def calculate_buyer_rank(self):
        # میانگین هزینه‌های مشتریانی که خرید داشته‌اند
        global_avg = Factors.objects.filter(costumer__factor__isnull=False) \
            .aggregate(avg_price=Avg('price'))['avg_price'] or 0
            
        print(global_avg)

        # مجموع هزینه‌های مشتری جاری
        customer_spent = self.factor.aggregate(total_spent=Sum('price'))['total_spent'] or 0

        # تعیین رنک بر اساس میانگین
        if customer_spent > global_avg:
            return CustomerProfile.GOLD
        elif customer_spent < global_avg:
            return CustomerProfile.SILVER
        else:
            return CustomerProfile.BRONZE
    
    def destroy(self, request, *args, **kwargs):
        print(f"User's work_position: {getattr(request.user.profile, 'work_position', 'No Profile')}")

        if hasattr(request.user, 'profile') and request.user.profile.work_position == 'regular':
            raise PermissionDenied("Employees are not allowed to delete customer profiles.")
        
        return super().destroy(request, *args, **kwargs)
    
    