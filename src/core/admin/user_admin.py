from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from core.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (
            _('Base info'),
            {
                'fields': ('username', 'password')
            }
        ),
        (
            _('Personal info'),
            {
                'fields': ('first_name', 'last_name', 'email')
            }
        ),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            }
        ),
        (
            _('Important dates'),
            {
                'fields': ('last_login', 'date_joined')
            }
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'password1', 'password2'),
            }
        ),
    )

    list_display = [
        'username', 'email', 'first_name', 'last_name', 'is_staff'
    ]
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    readonly_fields = ['date_joined', 'last_login']
