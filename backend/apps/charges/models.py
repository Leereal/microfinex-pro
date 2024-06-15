from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.audits.auditing import AuditableMixin

from apps.common.models import TimeStampedModel
from apps.loan_statuses.models import LoanStatus

class Charge(TimeStampedModel, AuditableMixin):
    AMOUNT_TYPE_CHOICES = [
        ('fixed', _('Fixed')),
        ('percentage', _('Percentage')),
    ]
    CHARGE_TYPE_CHOICES = [
        ('credit', _('Credit')),
        ('debit', _('Debit')),
    ]
    # FREQUENCY_CHOICES = [
    #     ('one-time', _('One-time')),
    #     ('recurring', _('Recurring')),
    # ]
    MODE_CHOICES = [
        ('manual', _('Manual')),
        ('auto', _('Auto')),
    ]
    APPLICATION_CHOICES = [
        ('principal', _('Principal')),
        ('balance', _('Balance')),
        ('other', _('Other')),
    ]

    name = models.CharField(_("Name"), max_length=255, unique=True)
    description = models.TextField(_("Description"), blank=True, null=True)
    amount = models.DecimalField(_("Amount"), max_digits=15, decimal_places=2) 
    # This is whether the charge is calculated based on fixed amount or percentage of amount (check charge application )   
    amount_type = models.CharField(_("Amount Type"), max_length=20, choices=AMOUNT_TYPE_CHOICES)   
    # This is either a charge (debit) or a bonus (credit)
    charge_type = models.CharField(_("Charge Type"), max_length=20, choices=CHARGE_TYPE_CHOICES)
    # This is where we apply the charge / bonus is it on balance or the principal amount
    charge_application = models.CharField(_("Charge Application"), max_length=20, choices=APPLICATION_CHOICES, default='principal')
    # This is the status in which the charge is applied to
    loan_status = models.ForeignKey(LoanStatus, verbose_name=_("Loan Status"), on_delete=models.SET_NULL, related_name='charges', blank=True, null=True)   
    # This is to know if we are supposed to apply the charge only once or everytime when the loan is still in that same status

    #If one-time option we must check if the charge was not already added and if not we add 
    # frequency = models.CharField(_("Frequency"), max_length=20, choices=FREQUENCY_CHOICES) 
       
    #This is to know when to use the charge if it's auto then it means we use it with the engine if manual then it's applied by users only
    mode = models.CharField(_("Mode"), max_length=20, choices=MODE_CHOICES)    
    is_active = models.BooleanField(_("Is Active"), default=True)

    class Meta:
        verbose_name = _("Charge")
        verbose_name_plural = _("Charges")

    def __str__(self):
        return self.name
    
    def get_audit_fields(self):
        # Dynamically retrieve all field names from the model
        return [field.name for field in self._meta.fields]
