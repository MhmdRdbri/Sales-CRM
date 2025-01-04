from django.contrib import admin
from .models import SalesOpportunity, SalesOpportunityItem


class SalesOpportunityItemInline(admin.TabularInline):
    model = SalesOpportunityItem
    extra = 1  # Number of empty rows to display for adding new items
    fields = ['product', 'quantity']  # Fields to display in the inline form
    show_change_link = True  # Allow linking to the individual items for editing


@admin.register(SalesOpportunity)
class SalesOpportunityAdmin(admin.ModelAdmin):
    list_display = ('id', 'follow_up_date', 'estimated_amount', 'opportunity_priority', 'profile')
    search_fields = ('profile__name', 'opportunity_priority')
    list_filter = ('opportunity_priority', 'created_at')
    date_hierarchy = 'created_at'
    inlines = [SalesOpportunityItemInline]  # Add the inline for SalesOpportunityItem
    readonly_fields = ['created_at']  # Make created_at readonly
    fieldsets = (
        (None, {
            'fields': ('follow_up_date', 'estimated_amount', 'opportunity_priority', 'profile', 'description')
        }),
        ('Date Information', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
