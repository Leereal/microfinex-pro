from decimal import Decimal
from django.db import models
from apps import group_product
from apps.audits.auditing import AuditableMixin
from apps.branch_products.models import BranchProduct
from apps.clients.models import Client
from apps.group_product.models import GroupProduct
from apps.loans.disburse import disburse_loan
from apps.products.models import Product
from apps.branches.models import Branch
from django.contrib.auth import get_user_model
from apps.currencies.models import Currency
from apps.loan_applications.models import LoanApplication
from apps.loan_statuses.models import LoanStatus
from apps.common.models import TimeStampedModel
from apps.loan_transactions.models import LoanTransaction
from django.db.models import Sum

User = get_user_model()

class Loan(TimeStampedModel, AuditableMixin):
    client = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE, 
        related_name='loans',
        verbose_name='Client',
        help_text='The client to whom the loan is issued.'
    )  
    branch_product = models.ForeignKey(
        BranchProduct,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Branch Product',
        help_text='The branch product associated with this loan.'
    )
    group_product = models.ForeignKey(
        GroupProduct,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Group Product',
        help_text='The group product associated with this loan.'
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='created_loans',
        verbose_name='Created by',
        help_text='The staff member who created this loan record.'
    )
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='approved_loans', 
        blank=True, 
        null=True,
        verbose_name='Approved by',
        help_text='The staff member who approved this loan. Null if not yet approved.'
    )
    amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2,
        verbose_name='Amount',
        help_text='The total amount of the loan.'
    )   
    interest_rate = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='Interest Rate',
        help_text='The interest rate of the loan.',
        blank=True,
        null=True
    )
    interest_amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2,
        verbose_name='Interest Amount',
        help_text='The total amount of interest applied to the loan.',
        blank=True,
        null=True
    )
    currency = models.ForeignKey(
        Currency, 
        on_delete=models.CASCADE,
        verbose_name='Currency',
        help_text='The currency in which the loan is issued.'
    )
    loan_application = models.ForeignKey(
        LoanApplication, 
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Loan Application',
        help_text='The loan application associated with this loan.'
    )
    disbursement_date = models.DateTimeField(
        verbose_name='Disbursement Date',
        help_text='The date and time when the loan was disbursed.'
    )
    start_date = models.DateTimeField(
        verbose_name='Start Date',
        help_text='The date and time when the loan period start'
    )    
    expected_repayment_date = models.DateTimeField(
        verbose_name='Repayment Date',
        help_text='The expected date and time for the loan to be fully repaid.'
    )
    next_due_date = models.DateTimeField(
        blank = True,
        null = True,
        verbose_name='Next Due Date',
        help_text='The date and time when the next payment is due.'
    )
    status = models.ForeignKey(
        LoanStatus, 
        on_delete=models.CASCADE,
        verbose_name='Status',
        help_text='The current status of the loan.',
        default=LoanStatus.objects.get(name='Pending').id                
    )
    branch = models.ForeignKey(
        Branch, 
        on_delete=models.CASCADE, 
        related_name='branch_loans',
        verbose_name='Branch',
        help_text='The branch through which the loan was issued.'
    )

    class Meta:
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'

    def __str__(self):
        return f"Loan ID: {self.id}, Client: {self.client}, Group Product: {self.group_product}, Branch Product: {self.branch_product}"
    
    def get_audit_fields(self):
        # Dynamically retrieve all field names from the model
        return [field.name for field in self._meta.fields]
    
    @property
    def total_payments(self):
        """Get sum of all payments for this loan."""
        return self.loan_transactions.filter(transaction_type=LoanTransaction.TransactionType.REPAYMENT).aggregate(Sum('debit'))['debit__sum'] or Decimal('0.00')
    
    @property
    def total_charges(self):
        """Get sum of all charges for this loan."""
        return self.loan_transactions.filter(transaction_type=LoanTransaction.TransactionType.CHARGE).aggregate(Sum('debit'))['debit__sum'] or Decimal('0.00')

    @property
    def total_bonuses(self):
        """Get sum of all bonuses for this loan."""
        return self.loan_transactions.filter(transaction_type=LoanTransaction.TransactionType.BONUS).aggregate(Sum('credit'))['credit__sum'] or Decimal('0.00')

    @property
    def balance(self):
        """Calculate the balance for this loan."""
        total_debits = self.loan_transactions.aggregate(Sum('debit'))['debit__sum'] or Decimal('0.00')
        total_credits = self.loan_transactions.aggregate(Sum('credit'))['credit__sum'] or Decimal('0.00')
        return total_debits - total_credits
     
    def save(self, *args, **kwargs):        
        super().save(*args, **kwargs)
        if self.status.name == 'Pending' or self.status.name == 'Approved':
            disburse_loan(self)
   
