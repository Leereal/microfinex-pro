from django.contrib import admin
from .models import Group

class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'leader', 'email', 'phone', 'is_active', 'branch', 'created_by', 'status', 'created_at', 'last_modified')
    list_filter = ('is_active', 'branch', 'created_by', 'status', 'created_at')
    search_fields = ('name', 'description', 'leader', 'email', 'phone')
    readonly_fields = ('created_at', 'last_modified')

admin.site.register(Group, GroupAdmin)
