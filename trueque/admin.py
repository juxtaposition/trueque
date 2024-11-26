from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUsers
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (_('Personal info'), {'fields': ('first_name', 'email', 'last_name', 'username')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(CustomUsers, CustomUserAdmin)
