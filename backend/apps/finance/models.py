from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from apps.audits.auditing import AuditableMixin
from apps.branches.models import Branch
from apps.common.models import TimeStampedModel
from django.db.models import Sum, Count

from apps.loan_transactions.models import LoanTransaction

User = get_user_model()

class Finance(TimeStampedModel, AuditableMixin):
    class Type(models.TextChoices):
        INCOME = 'income', _('Income')
        EXPENSE = 'expense', _('Expense')
        INVESTMENT = 'investment', _('Investment')
        WITHDRAWAL = 'withdrawal', _('Withdrawal')

    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'), blank=True, null=True)
    amount = models.DecimalField(_('Amount'), max_digits=15, decimal_places=2)
    received_from = models.CharField(_('Received From'), max_length=255, blank=True, null=True)
    paid_to = models.CharField(_('Paid To'), max_length=255, blank=True, null=True)
    receipt_number = models.CharField(_('Receipt Number'), max_length=255, blank=True, null=True)
    receipt_screenshot = models.CharField(_('Receipt Screenshot'), max_length=255, blank=True, null=True)
    type = models.CharField(_('Type'), max_length=20, choices=Type.choices)
    created_by = models.ForeignKey(User, verbose_name=_('Created By'), on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, verbose_name=_('Branch'), on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Finance')
        verbose_name_plural = _('Finances')

    @staticmethod
    def calculate_available_funds(branch_id):
        income = Finance.objects.filter(type='income', branch_id=branch_id).aggregate(Sum('amount'))['amount__sum'] or 0
        investments = Finance.objects.filter(type='investment', branch_id=branch_id).aggregate(Sum('amount'))['amount__sum'] or 0
        expense = Finance.objects.filter(type='expense', branch_id=branch_id).aggregate(Sum('amount'))['amount__sum'] or 0
        withdrawal = Finance.objects.filter(type='withdrawal', branch_id=branch_id).aggregate(Sum('amount'))['amount__sum'] or 0

        # Calculate total LoanTransaction repayments
        loan_repayments = LoanTransaction.objects.filter(
            transaction_type='repayment', 
            branch_id=branch_id
        ).aggregate(Sum('debit'))['debit__sum'] or 0

        # Calculate total LoanTransaction charges where credit is not null
        charges = LoanTransaction.objects.filter(
            transaction_type='charge', 
            branch_id=branch_id, 
            credit__isnull=False
        ).aggregate(Sum('credit'))['credit__sum'] or 0

        # Calculate total disbursements
        disbursements = LoanTransaction.objects.filter(
            transaction_type='disbursement', 
            branch_id=branch_id
        ).aggregate(Sum('debit'))['debit__sum'] or 0

        # Calculate available funds
        available_funds = income + investments - expense - withdrawal + loan_repayments - disbursements + charges
        return available_funds

    def get_audit_fields(self):
        # Dynamically retrieve all field names from the model
        return [field.name for field in self._meta.fields]

    
