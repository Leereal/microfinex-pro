from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.audits.auditing import AuditableMixin
from apps.common.models import TimeStampedModel
from apps.branches.models import Branch
from apps.clients.models import Client

User = get_user_model()

class LoanApplication(TimeStampedModel, AuditableMixin):
    """
    Represents a loan application made by a client.
    """
    class Status(models.TextChoices):
        REJECTED = 'rejected', _('Rejected')
        APPROVED = 'approved', _('Approved')
        PENDING = 'pending', _('Pending')
        CANCELLED = 'cancelled', _('Cancelled')

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='loan_applications', verbose_name=_('Client'))
    amount = models.DecimalField(_('Amount'), max_digits=15, decimal_places=2, help_text=_('Total loan amount applied for.'))
    status = models.CharField(_('Status'), max_length=20, choices=Status.choices, default=Status.PENDING, help_text=_('Current status of the loan application.'))
    rejection_reason = models.ForeignKey('RejectionReason', on_delete=models.SET_NULL, null=True, blank=True, related_name='loan_applications', verbose_name=_('Rejection Reason'))
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='loan_applications', verbose_name=_('Processed By'))
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='loan_applications', verbose_name=_('Branch'))

    def __str__(self):
        return f"Loan Application {self.id} - {self.client} - Status: {self.status}"
    
    class Meta:
        verbose_name = _('Loan Application')
        verbose_name_plural = _('Loan Applications')
    
    def get_audit_fields(self):
        # Dynamically retrieve all field names from the model
        return [field.name for field in self._meta.fields]

class RejectionReason(TimeStampedModel):
    """
    Stores reasons for loan application rejections.
    """
    title = models.CharField(_('Title'), max_length=255, help_text=_('Short title for the rejection reason.'))
    description = models.TextField(_('Description'), help_text=_('Detailed description of the rejection reason.'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rejection_reasons', verbose_name=_('Created By'))

    def __str__(self):
        return self.title
