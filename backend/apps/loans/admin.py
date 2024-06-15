from django.contrib import admin
from apps.documents.models import Document

from apps.loan_statuses.models import LoanStatus
from .models import Loan
from django.utils.html import format_html

class DocumentInline(admin.StackedInline):  # or use TabularInline for a more compact layout
    model = Document
    extra = 1  # How many empty rows to show
    fields = ['name', 'file', 'document_type','expiration_date']  # Adjust fields as needed


class LoanAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'client', 'amount', 'interest_rate', 'interest_amount',
        'currency', 'status', 'branch', 'created_by', 'approved_by', 'disbursement_date',
        'start_date', 'expected_repayment_date', 'next_due_date', 'total_payments_display',
        'total_charges_display', 'total_bonuses_display', 'balance_display'
    )
    list_filter = (
        'client', 'currency', 'status', 'branch', 'created_by', 'approved_by'
    )
    list_display_links = ('id', 'client')
    search_fields = (
        'client__name', 'currency__code', 'status__name', 'branch__name',
        'created_by__username', 'approved_by__username'
    )
    readonly_fields = (
        'total_payments', 'total_charges', 'total_bonuses', 'balance',
        'created_at', 'last_modified'
    )
    inlines = [DocumentInline]

    @admin.display(description='Total Payments')
    def total_payments_display(self, obj):
        return format_html("<strong>{}</strong>", obj.total_payments)

    @admin.display(description='Total Charges')
    def total_charges_display(self, obj):
        return format_html("<strong>{}</strong>", obj.total_charges)

    @admin.display(description='Total Bonuses')
    def total_bonuses_display(self, obj):
        return format_html("<strong>{}</strong>", obj.total_bonuses)

    @admin.display(description='Balance')
    def balance_display(self, obj):
        return format_html("<strong>{}</strong>", obj.balance)

    actions = ['approve_and_disburse_loans']

    @admin.action(description='Approve and disburse selected loans')
    def approve_and_disburse_loans(self, request, queryset):
        for loan in queryset:
            loan.status = LoanStatus.objects.get(name='Approved')  # Assuming 'approved' is a status instance
            
            loan.save()  # The save method now includes check_and_disburse logic

    

admin.site.register(Loan, LoanAdmin)
