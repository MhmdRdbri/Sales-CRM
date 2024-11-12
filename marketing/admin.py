from django.contrib import admin
from .models import *


@admin.register(Marketing)
class MarketingAdmin(admin.ModelAdmin):
    list_display = ['id', 'campaign_name', 'start_date', 'end_date',]
    search_fields = ['campaign_name', 'start_date',"end_date"] 
    fieldsets = (
        (None, {
            'fields': ('campaign_name', 'message', 'target_audiences')
        }),
        ('Date Information', {
            'fields': ('start_date','end_date'),
            'classes': ('collapse',),
        }),
    )
