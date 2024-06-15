from django.contrib import admin
from .models import GlobalSettings

@admin.register(GlobalSettings)
class GlobalSettingsAdmin(admin.ModelAdmin):
    list_display = [
        'company_name', 'contact_email', 'contact_phone', 'default_interest_rate',
        'min_loan_amount', 'max_loan_amount', 'loan_approval_required',
        'loan_application_allowed', 'fiscal_year_start', 'fiscal_year_end',
        'currency_code', 'timezone'
    ]
    fieldsets = (
        ('Company Information', {
            'fields': ('company_name', 'company_logo', 'contact_email', 'contact_phone', 'address')
        }),
        ('Loan Settings', {
            'fields': ('default_interest_rate', 'min_loan_amount', 'max_loan_amount',
                       'loan_approval_required', 'loan_application_allowed')
        }),
        ('Fiscal Year', {
            'fields': ('fiscal_year_start', 'fiscal_year_end')
        }),
        ('System Defaults', {
            'fields': ('currency_code', 'timezone')
        }),
    )
    search_fields = ['company_name', 'contact_email', 'currency_code']
