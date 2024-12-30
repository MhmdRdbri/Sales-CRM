from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from marketing.models import Marketing
from factors.models import *
from customerprofile.models import CustomerProfile
from salesopportunities.models import SalesOpportunity
from rest_framework import status
from django.db.models import Sum, Count,Min
from datetime import date

class DashboardDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Marketing status counts
        marketing_status_counts = Marketing.objects.values('status').annotate(count=Count('status'))
        marketing_data = {status['status']: status['count'] for status in marketing_status_counts}

        # Factors and products sold
        total_factors = Factors.objects.count()
        total_products_sold = FactorItem.objects.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
        total_sales = Factors.objects.aggregate(total_price=Sum('price'))['total_price'] or 0

        # Customer count
        total_customers = CustomerProfile.objects.count()

        # Closest sales opportunity count
        closest_opportunity_date = SalesOpportunity.objects.filter(
            follow_up_date__gte=date.today()
        ).aggregate(closest_date=Min('follow_up_date'))['closest_date']

        closest_opportunity_count = SalesOpportunity.objects.filter(
            follow_up_date=closest_opportunity_date
        ).count() if closest_opportunity_date else 0

        # Prepare the response
        response_data = {
            "marketing_status": marketing_data,
            "sales_data": {
                "total_factors": total_factors,
                "total_products_sold": total_products_sold,
                "total_sales": total_sales,
            },
            "customer_data": {
                "total_customers": total_customers,
            },
            "sales_opportunity": {
                "closest_count": closest_opportunity_count,
            },
        }

        return Response(response_data, status=200)
