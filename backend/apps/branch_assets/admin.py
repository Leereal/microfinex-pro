from django.contrib import admin
from .models import BranchAssets

@admin.register(BranchAssets)
class BranchAssetsAdmin(admin.ModelAdmin):
    list_display = ('id', 'branch', 'item', 'brand', 'color', 'quantity', 'user', 'used_by', 'purchase_date', 'created_at', 'last_modified', 'deleted_at')
    list_filter = ('branch', 'user', 'used_by', 'purchase_date', 'created_at','last_modified', 'deleted_at')
    search_fields = ('item', 'brand', 'color')
    readonly_fields = ('created_at','last_modified', 'deleted_at')
