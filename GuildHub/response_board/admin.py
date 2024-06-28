from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Response


class ResponseTranslation(TranslationAdmin):
    model = Response


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('author', 'ad', 'status', 'date_creation', 'date_status_change')
    list_filter = ('status', 'date_creation', 'date_status_change')
    search_fields = ('author', 'ad')
    ordering = ('-date_creation',)
