from django.contrib import admin
from .models import Factor, FactorItem


class FactorItemInline(admin.TabularInline):
    model = FactorItem
    extra = 1  # Number of empty forms to display in the admin interface


@admin.register(Factor)
class FactorAdmin(admin.ModelAdmin):
    list_display = ('id', 'contract_date', 'price', 'customer', 'file_display', 'description_preview')
    list_filter = ('contract_date', 'customer')
    search_fields = ('description', 'customer__name')  # Assuming `CustomerProfile` has a `name` field
    inlines = [FactorItemInline]

    def file_display(self, obj):
        if obj.file:
            return f"<a href='{obj.file.url}' target='_blank'>Download File</a>"
        return "No File"
    file_display.allow_tags = True
    file_display.short_description = "File"

    def description_preview(self, obj):
        return obj.description[:50] + "..." if obj.description else "No Description"
    description_preview.short_description = "Description"


@admin.register(FactorItem)
class FactorItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'factor', 'product', 'quantity')
    list_filter = ('factor', 'product')
    search_fields = ('factor__id', 'product__product_name')
