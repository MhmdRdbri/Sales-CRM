from django.contrib import admin
from .models import *


class FactorItemInline(admin.TabularInline):
    model = FactorItem
    extra = 1 
    fields = ['product', 'quantity']  
    show_change_link = True

@admin.register(Factors)
class FactorsAdmin(admin.ModelAdmin):
    list_display = ['id', 'costumer', 'price', 'contract_date',]
    search_fields = ['costumer__name', 'description'] 
    list_filter = ['contract_date']
    inlines = [FactorItemInline]  
    readonly_fields = ['contract_date'] 
    fieldsets = (
        (None, {
            'fields': ('costumer', 'price', 'description')
        }),
        ('Date Information', {
            'fields': ('contract_date',),
            'classes': ('collapse',),
        }),
    )
