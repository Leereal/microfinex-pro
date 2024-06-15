from django.contrib import admin
from .models import BranchProduct

@admin.register(BranchProduct)
class BranchProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'branch', 'product', 'interest', 'max_amount', 'min_amount', 'period', 'min_period', 'max_period', 'is_active', 'created_by', 'created_at', 'last_modified')
    list_filter = ('branch', 'product', 'period', 'is_active', 'created_by', 'last_modified', 'deleted_at')
    search_fields = ('branch__name', 'product__name')
    readonly_fields = ('created_at', 'last_modified')
