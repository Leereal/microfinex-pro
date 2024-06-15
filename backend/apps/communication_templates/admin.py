from django.contrib import admin
from .models import CommunicationTemplates

@admin.register(CommunicationTemplates)
class CommunicationTemplatesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type', 'is_active', 'created_at', 'deleted_at')
    list_filter = ('type', 'is_active', 'created_at', 'deleted_at')
    search_fields = ('title',)
    readonly_fields = ('created_at', 'deleted_at')
