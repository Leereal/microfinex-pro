from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.audits.auditing import AuditableMixin
from apps.common.models import TimeStampedModel

class PaymentGateway(TimeStampedModel, AuditableMixin):
    class Type(models.TextChoices):
        ONLINE = 'online', _('Online')
        OFFLINE = 'offline', _('Offline')

    name = models.CharField(_("Name"), max_length=255, unique=True, help_text=_("Unique name for the payment gateway."))
    description = models.TextField(_("Description"), blank=True, null=True, help_text=_("Description of the payment gateway."))
    type = models.CharField(_("Type"), max_length=20, choices=Type.choices, help_text=_("Type of the payment gateway (Online/Offline)."))
    is_disbursement = models.BooleanField(_("Is Disbursement"), default=False, help_text=_("Indicates if the gateway is used for disbursements."))
    is_repayment = models.BooleanField(_("Is Repayment"), default=False, help_text=_("Indicates if the gateway is used for repayments."))
    is_active = models.BooleanField(_("Is Active"), default=True, help_text=_("Indicates if the payment gateway is active."))

    class Meta:
        verbose_name = _("Payment Gateway")
        verbose_name_plural = _("Payment Gateways")

    def __str__(self):
        return self.name
    
    def get_audit_fields(self):
        # Dynamically retrieve all field names from the model
        return [field.name for field in self._meta.fields]
