from django.contrib import admin
from .models import LoanApplication, RejectionReason

class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'amount', 'status', 'rejection_reason', 'user', 'branch', 'created_at', 'last_modified')
    list_display_links = ('id', 'client', 'branch')
    list_filter = ('status', 'user', 'branch', 'created_at', 'last_modified')
    search_fields = ('client__name', 'amount')
    readonly_fields = ('created_at','last_modified')

admin.site.register(LoanApplication, LoanApplicationAdmin)
admin.site.register(RejectionReason)
