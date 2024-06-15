from django.contrib import admin

from .models import Finance

class FinanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'amount', 'type', 'created_by', 'branch_id', 'created_at', 'last_modified')
    list_filter = ('type', 'created_by', 'branch_id', 'created_at', 'last_modified')
    search_fields = ('title', 'description', 'received_from', 'paid_to', 'receipt_number')
    readonly_fields = ('created_at', 'last_modified')

admin.site.register(Finance, FinanceAdmin)
