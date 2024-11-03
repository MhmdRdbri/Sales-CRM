from django.contrib import admin
from .models import SalesOpportunity

@admin.register(SalesOpportunity)
class SalesOpportunityAdmin(admin.ModelAdmin):
    list_display = ('id', 'follow_up_date', 'estimated_amount', 'opportunity_priority', 'profile')
    search_fields = ('profile__name', 'opportunity_priority')  # assuming CustomerProfile has a 'name' field
    list_filter = ('opportunity_priority', 'created_at')
    date_hierarchy = 'created_at'
