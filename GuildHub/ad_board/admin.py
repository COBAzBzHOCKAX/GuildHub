from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Ad, Category


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_title', 'category', 'get_user_nickname', 'user',
                    'is_published', 'date_published', 'date_creation')
    list_display_links = ('id', 'short_title')
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'text', 'user__nickname', 'user__email')

    def get_user_nickname(self, obj):
        return obj.user.nickname if obj.user.nickname else None

    get_user_nickname.short_description = _('Nickname')
    Ad.short_title.short_description = _('Title')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name',)
    list_display_links = ('id', 'category_name')
    list_filter = ('category_name',)
    search_fields = ('category_name',)
