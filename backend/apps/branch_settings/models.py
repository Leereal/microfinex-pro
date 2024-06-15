from django.db import models
from apps.branches.models import Branch
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedModel

class BranchSettings(TimeStampedModel):
    branch = models.OneToOneField(Branch, on_delete=models.CASCADE, related_name='settings', verbose_name="Branch")
    loan_approval_required = models.BooleanField(default=True, help_text="Indicates if loans require approval before disbursement for this branch.")
    loan_application_allowed = models.BooleanField(default=True, help_text="Indicates if loan applications are allowed for this branch.")
    min_loan_amount = models.DecimalField(max_digits=15, decimal_places=2, help_text="Minimum loan amount applicable for this branch.")
    max_loan_amount = models.DecimalField(max_digits=15, decimal_places=2, help_text="Maximum loan amount applicable for this branch.")
    default_interest_rate = models.DecimalField(max_digits=5, decimal_places=2,validators=[MinValueValidator(0.0), MaxValueValidator(100.0)], help_text="Default interest rate for loans for this branch.")

    class Meta:
        verbose_name = _("Branch Setting")
        verbose_name_plural = _("Branch Settings")

    def __str__(self):
        return f"{self.branch.name} Settings"
