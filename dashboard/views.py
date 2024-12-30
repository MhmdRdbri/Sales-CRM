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
import jdatetime
from django.db.models.functions import TruncMonth

class DashboardDetail(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_customer_data(self):
        """
        محاسبه تعداد مشتریان جذب‌شده بر اساس ماه‌های شمسی
        """
        customers = CustomerProfile.objects.all()
        monthly_data = {}

        for customer in customers:
            if customer.created_at:
                shamsi_date = jdatetime.date.fromgregorian(date=customer.created_at)
                month_key = f"{shamsi_date.year}-{shamsi_date.month}"

                if month_key not in monthly_data:
                    monthly_data[month_key] = 0
                monthly_data[month_key] += 1

        # مرتب‌سازی داده‌ها بر اساس سال-ماه
        sorted_monthly_data = dict(sorted(monthly_data.items()))
        return sorted_monthly_data 
    
    def get_sales_data(self):
        """
        محاسبه تغییرات فروش در طول سال (بر اساس ماه‌های شمسی)
        """
        sales_data = {}

        # برای هر فاکتور، مجموع قیمت‌ها را بر اساس ماه شمسی جمع‌آوری می‌کنیم
        factors = Factors.objects.all()
        for factor in factors:
            # تبدیل تاریخ فاکتور به تاریخ شمسی
            shamsi_date = jdatetime.date.fromgregorian(date=factor.contract_date)
            month_key = f"{shamsi_date.year}-{shamsi_date.month}"

            if month_key not in sales_data:
                sales_data[month_key] = 0
            sales_data[month_key] += factor.price

        # مرتب‌سازی داده‌ها بر اساس سال-ماه
        sorted_sales_data = dict(sorted(sales_data.items()))
        return sorted_sales_data
    

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
        
        customer_chart_data = self.get_customer_data()
        
        labels = list(customer_chart_data.keys())  # سال-ماه
        counts = list(customer_chart_data.values())  # تعداد مشتریان
        
        sales_data = self.get_sales_data()
        
        
        sales_labels = list(sales_data.keys())  # سال-ماه
        sales_values = list(sales_data.values())  # مجموع قیمت فروش

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
            "customer_chart": {
                "labels": labels,
                "data": counts
            },
            "sales_chart": {
                "labels": sales_labels,
                "data": sales_values
            }            
            
        }

        return Response(response_data, status=200)
