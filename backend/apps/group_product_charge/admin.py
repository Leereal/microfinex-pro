from django.contrib import admin
from .models import GroupProductCharge

@admin.register(GroupProductCharge)
class GroupProductChargeAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_product', 'charge', 'is_active', 'last_modified')
    list_filter = ('group_product', 'charge', 'is_active', 'last_modified')
    readonly_fields = ('created_at','last_modified')
