from django.contrib import admin
from .models import CustomUser, Profile, PasswordResetToken

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

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'work_position', 'department', 'telegram_id', 'created_at')
    search_fields = ('user__full_name', 'work_position', 'department')
    list_filter = ('work_position', 'department', 'created_at')
    ordering = ('-created_at',)

class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at')
    search_fields = ('user__full_name', 'token')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

# Register models with the admin site
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(PasswordResetToken, PasswordResetTokenAdmin)
