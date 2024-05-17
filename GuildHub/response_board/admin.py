from django.contrib import admin

from .models import Response


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('author', 'ad', 'status', 'date_creation', 'date_status_change')
    list_filter = ('status', 'date_creation', 'date_status_change')
    search_fields = ('author', 'ad')
    ordering = ('-date_creation',)
