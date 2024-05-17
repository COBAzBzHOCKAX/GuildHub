from config import settings
from django.apps import apps
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

UserModel = apps.get_model(*settings.AUTH_USER_MODEL.split('.', 1))


class CustomUserAdmin(UserAdmin):
    model = UserModel

    list_display = ('id', 'email', 'nickname', 'age', 'is_staff', 'is_active',)
    list_display_links = ('id', 'email', 'nickname')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('nickname', 'email')
    ordering = ('email',)

    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        (_('Permissions'), {
            'fields': ('is_staff', 'is_active')
        }),
        (_('Personal info'), {
            'fields': (
                'first_name', 'last_name', 'nickname', 'date_birth', 'phone_number',
                'discord_url_profile', 'about_me'
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
