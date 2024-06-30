from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from .models import Newsletter


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_title', 'short_text', 'author', 'date_creation', 'is_published')
    list_display_links = ('id', 'short_title', 'short_text')
    list_filter = ('author',)
    search_fields = ('title', 'text')
    ordering = ('-date_creation',)

    Newsletter.short_title.short_description = _('Title')
    Newsletter.short_text.short_description = _('Text')
