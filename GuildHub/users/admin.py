from config import settings
from django.apps import apps
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

UserModel = apps.get_model(*settings.AUTH_USER_MODEL.split('.', 1))


class CustomUserAdmin(UserAdmin):
    model = UserModel

    list_display = ('id', 'email', 'nickname', 'age', 'is_staff', 'is_active', 'is_banned')
    list_display_links = ('id', 'email', 'nickname')
    list_filter = ('is_staff', 'is_active', 'is_banned')
    search_fields = ('nickname', 'email', 'first_name', 'last_name', 'phone_number', 'discord_url_profile')
    ordering = ('email',)

    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        (_('Personal info'), {
            'fields': (
                'avatar', 'nickname', 'first_name', 'last_name', 'gender', 'date_birth', 'phone_number',
                'discord_url_profile', 'about_me'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_staff',
                'is_active',
                'is_superuser',
                'is_banned',
                'banned_until',
                "groups",
                "user_permissions",
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nickname', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )


admin.site.register(UserModel, CustomUserAdmin)
