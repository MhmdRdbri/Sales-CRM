from django.contrib import admin
from .models import *

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'email', 'buyer_rank')
    search_fields = ('full_name', 'email', 'phone_number')
    list_filter = ('buyer_rank',)