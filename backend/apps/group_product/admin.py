from django.contrib import admin
from .models import GroupProduct

@admin.register(GroupProduct)
class GroupProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'product', 'interest', 'max_amount', 'min_amount', 'period', 'min_period', 'max_period', 'is_active', 'created_by', 'created_at', 'last_modified')
    list_filter = ('group', 'product', 'period', 'is_active', 'created_by', 'created_at', 'last_modified')
    search_fields = ('group__name', 'product__name', 'created_by__username')
    readonly_fields = ('created_at', 'last_modified')
