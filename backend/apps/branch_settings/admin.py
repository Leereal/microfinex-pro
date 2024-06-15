from django.contrib import admin
from .models import BranchSettings

@admin.register(BranchSettings)
class BranchSettingsAdmin(admin.ModelAdmin):
    list_display = ['branch', 'loan_approval_required', 'loan_application_allowed', 'min_loan_amount', 'max_loan_amount', 'default_interest_rate']
    list_filter = ['loan_approval_required', 'loan_application_allowed', 'branch']
    search_fields = ['branch__name']
    fieldsets = (
        (None, {
            'fields': ('branch', 'loan_approval_required', 'loan_application_allowed')
        }),
        ('Loan Amount Settings', {
            'fields': ('min_loan_amount', 'max_loan_amount', 'default_interest_rate')
        }),
    )

    def get_queryset(self, request):
        # Customize the queryset if needed, for example, to show only branches the user is allowed to manage
        qs = super().get_queryset(request)
        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Customize the dropdowns if needed, e.g., limit choices for the branch field
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
