from django.db import models

from apps.common.models import TimeStampedModel

class GlobalSettings(TimeStampedModel):
    company_name = models.CharField(max_length=255, help_text="The name of the company using the loan management system.")
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True, help_text="The company logo.")
    contact_email = models.EmailField(help_text="Primary contact email for the company.")
    contact_phone = models.CharField(max_length=20, help_text="Primary contact phone number for the company.")
    address = models.TextField(help_text="Company's physical address.")

    default_interest_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Default global interest rate for loans.")
    min_loan_amount = models.DecimalField(max_digits=15, decimal_places=2, help_text="Minimum loan amount applicable globally.")
    max_loan_amount = models.DecimalField(max_digits=15, decimal_places=2, help_text="Maximum loan amount applicable globally.")
    loan_approval_required = models.BooleanField(default=True, help_text="Indicates if loans require approval before disbursement globally.")
    loan_application_allowed = models.BooleanField(default=True, help_text="Indicates if loan applications are allowed globally.")

    fiscal_year_start = models.DateField(help_text="Start date of the fiscal year.")
    fiscal_year_end = models.DateField(help_text="End date of the fiscal year.")

    currency_code = models.CharField(max_length=3, default='USD', help_text="Default currency code for financial transactions.")
    timezone = models.CharField(max_length=50, default='UTC', help_text="The default timezone for the system operations.")

    class Meta:
        verbose_name = "Global Setting"
        verbose_name_plural = "Global Settings"

    def __str__(self):
        return self.company_name + " - Global Settings"
