from django.contrib import admin
from .models import SalesOpportunity

class SalesOpportunityAdmin(admin.ModelAdmin):
    list_display = ('id', 'follow_up_date', 'estimated_amount', 'opportunity_priority', 'created_at', 'profile')
    search_fields = ('profile__name', 'opportunity_priority')
    list_filter = ('opportunity_priority', 'created_at')

admin.site.register(SalesOpportunity, SalesOpportunityAdmin)
