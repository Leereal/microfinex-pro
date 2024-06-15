from enum import unique
from django.db import models
from apps.common.models import TimeStampedModel
from apps.currencies.models import Currency
from apps.payment_gateways.models import PaymentGateway
from apps.branches.models import Branch
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

User = get_user_model()

class LoanTransaction(TimeStampedModel):
    class TransactionType(models.TextChoices):
        DISBURSEMENT = 'disbursement', _('Disbursement')
        REPAYMENT = 'repayment', _('Repayment')
        INTEREST = 'interest', _('Interest')
        CHARGE = 'charge', _('Charge')
        REFUND = 'refund', _('Refund')
        BONUS = 'bonus', _('Bonus')     
        TOPUP = 'topup', _('Topup') 

    class TransactionStatus(models.TextChoices):
        REVIEW = 'review', _('Review')
        PENDING = 'pending', _('Pending')
        APPROVED = 'approved', _('Approved')
        CANCELLED = 'cancelled', _('Cancelled')
        REFUNDED = 'refunded', _('Refund')

    loan = models.ForeignKey('loans.Loan', on_delete=models.CASCADE, verbose_name=_('Loan'), related_name='loan_transactions')
    description = models.TextField(verbose_name=_('Description'), help_text=_('A brief description of the transaction.'), blank=True, null=True)
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices, verbose_name=_('Transaction Type'))
    debit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name=_('Debit Amount'), help_text=_('Amount debited (if applicable).'))
    credit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name=_('Credit Amount'), help_text=_('Amount credited (if applicable).'))
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name=_('Currency'))
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Created By'), blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))
    payment_gateway = models.ForeignKey(PaymentGateway, on_delete=models.CASCADE, verbose_name=_('Payment Gateway'), null=True, blank=True)
    status = models.CharField(max_length=20, choices=TransactionStatus.choices, verbose_name=_('Transaction Status'))

    class Meta:
        verbose_name = _('Loan Transaction')
        verbose_name_plural = _('Loan Transactions')
        constraints = [
            models.UniqueConstraint(
                fields=['loan'],
                condition=Q(transaction_type='disbursement'),
                name='unique_disbursement_per_loan'
            )
        ]

    def __str__(self):
        return f"Transaction ID: {self.id}, Loan: {self.loan}, Type: {self.transaction_type}"

