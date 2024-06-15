from django.contrib import admin
from .models import LoanTransaction

class LoanTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'loan', 'transaction_type','description', 'debit', 'credit', 'currency', 'created_by', 'branch', 'payment_gateway', 'status', 'created_at', 'last_modified', 'deleted_at')
    list_filter = ('transaction_type', 'currency', 'created_by', 'branch', 'payment_gateway', 'status', 'created_at', 'last_modified')
    search_fields = ('loan__id', 'transaction_type', 'status')
    readonly_fields = ('created_at', 'last_modified')

admin.site.register(LoanTransaction, LoanTransactionAdmin)
