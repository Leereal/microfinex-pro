from django.contrib import admin
from .models import Notifications

@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'receiver', 'sender', 'branch', 'message', 'is_viewed', 'created_at', 'deleted_at')
    list_filter = ('is_viewed', 'created_at', 'deleted_at')
    search_fields = ('message',)
    readonly_fields = ('created_at', 'deleted_at')
