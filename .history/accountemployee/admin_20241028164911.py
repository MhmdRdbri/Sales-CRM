from django.contrib import admin
from .models import *

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'email', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('full_name', 'phone_number', 'email')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {
            'fields': ('phone_number', 'full_name', 'email', 'is_active', 'is_staff')
        }),
        ('Permissions', {
            'fields': ('groups', 'user_permissions'),
        }),
        ('Date Information', {
            'fields': ('date_joined',),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'full_name', 'email', 'password', 'is_active', 'is_staff'),
        }),
    )
    filter_horizontal = ('groups', 'user_permissions')
    list_select_related = ('profile',)
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        profile_data = form.cleaned_data.get('profile')
        if profile_data:
            Profile.objects.update_or_create(user=obj, defaults=profile_data)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'work_position', 'department', 'telegram_id', 'created_at')
    search_fields = ('user__full_name', 'work_position', 'department')
    list_filter = ('work_position', 'department', 'created_at')
    ordering = ('-created_at',)

@admin.register(PasswordResetCode)
class PasswordResetCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'created_at']
    search_fields = ['user__phone_number', 'code']
    list_filter = ['created_at']

# Register models with the admin site
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)