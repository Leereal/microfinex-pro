from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.audits.auditing import AuditableMixin

from apps.common.models import TimeStampedModel

class LoanStatus(TimeStampedModel, AuditableMixin):
    name = models.CharField(
        max_length=100,
        verbose_name=_('Name'),
        help_text=_('The name of the loan status.')
    )
    description = models.TextField(
        verbose_name=_('Description'),
        help_text=_('A detailed description of the loan status.'),
        blank=True,  # Assuming you want to allow blank descriptions
        null=True
    )
    allow_auto_calculations = models.BooleanField(
        default=False,
        verbose_name=_('Allow Auto Calculations'),
        help_text=_('Indicates whether automatic calculations are allowed for this loan status.')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Is Active'),
        help_text=_('Indicates whether this loan status is active.')
    )

    class Meta:
        verbose_name = _('Loan Status')
        verbose_name_plural = _('Loan Statuses')

    def __str__(self):
        return self.name
    
    def get_audit_fields(self):
        # Dynamically retrieve all field names from the model
        return [field.name for field in self._meta.fields]
