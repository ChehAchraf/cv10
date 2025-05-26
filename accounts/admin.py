from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'full_name', 'is_premium', 'credits', 'date_joined', 'is_staff')
    search_fields = ('email', 'full_name')
    readonly_fields = ('date_joined',)
    
    filter_horizontal = ()
    list_filter = ('is_active', 'is_staff', 'is_premium')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('CV Platform', {'fields': ('is_premium', 'credits')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2'),
        }),
    )
    
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
