from django.contrib import admin
from .models import Sms

@admin.register(Smses)
class SmsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'client', 'loan', 'content', 'type', 'status', 'is_active', 'created_at', 'deleted_at')
    list_filter = ('status', 'type', 'is_active', 'created_at', 'deleted_at')
    search_fields = ('title', 'user__username', 'client__name', 'loan__id')
    readonly_fields = ('created_at', 'deleted_at')
