from django.contrib import admin
from .models import *


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ["id","title","text","send_time","send_date",]
    search_fields = ['title', 'audiences',"send_date"] 
    fieldsets = (
        (None, {
            'fields': ('title', 'text', 'audiences')
        }),
        ('Date Information', {
            'fields': ('send_date','send_time'),
            'classes': ('collapse',),
        }),
    )
