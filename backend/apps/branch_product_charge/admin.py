from django.contrib import admin
from .models import BranchProductCharge

@admin.register(BranchProductCharge)
class BranchProductChargeAdmin(admin.ModelAdmin):
    list_display = ('id', 'branch_product', 'charge', 'is_active', 'created_at', 'last_modified')
    list_filter = ('branch_product', 'charge', 'is_active', 'created_at', 'last_modified')
    readonly_fields = ('created_at', 'last_modified')
