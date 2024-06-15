from decimal import Decimal
from django.db import transaction
from apps.charges.models import Charge
from apps.loan_statuses.models import LoanStatus
from django.apps import apps
# from apps.loans.models import Loan
from apps.global_settings.models import GlobalSettings
from apps.branch_settings.models import BranchSettings
from apps.loan_transactions.models import LoanTransaction
from django.db import IntegrityError



def disburse_loan(loan):
      # Fetch global and branch-specific settings
    global_settings = GlobalSettings.objects.first()  # Assuming there's only one global settings instance
    branch_settings = loan.branch.settings if hasattr(loan.branch, 'settings') else None

    # Determine if loan approval is required
    loan_approval_required = branch_settings.loan_approval_required if branch_settings else global_settings.loan_approval_required

    
    # If loan approval is not required or loan is already approved, proceed with disbursement
    if not loan_approval_required or loan.status == LoanStatus.objects.get(name='Approved'):
        perform_disbursement(loan)

def perform_disbursement(loan):
    # LoanTransaction = apps.get_model('loan_transactions', 'LoanTransaction')
    product_charges = None  
    # Check if we have group product charges for this loan and if so, get the charges
    if loan.group_product:
        product_charges = loan.group_product.groupproductcharge_set.filter(charge__mode='auto', charge__is_active=True, charge__loan_status__name='Active')
    elif loan.branch_product:
        product_charges = loan.branch_product.branchproductcharge_set.filter(charge__mode='auto', charge__is_active=True, charge__loan_status__name='Active')

    try:       
        with transaction.atomic():
            # Create disbursement transaction
            LoanTransaction.objects.create(
                loan=loan,
                transaction_type=LoanTransaction.TransactionType.DISBURSEMENT,
                debit=loan.amount,
                currency=loan.currency,
                created_by=loan.created_by,
                branch=loan.branch,
                status=LoanTransaction.TransactionStatus.APPROVED,
                description="Loan disbursement"
            )

            # Calculate and record interest
            interest = loan.group_product.interest if loan.group_product else loan.branch_product.interest
            interest_amount = (loan.amount * interest / 100).quantize(Decimal('.01'))
            LoanTransaction.objects.create(
                loan=loan,
                transaction_type=LoanTransaction.TransactionType.INTEREST,
                debit=interest_amount,
                currency=loan.currency,
                created_by=loan.created_by,
                branch=loan.branch,
                status=LoanTransaction.TransactionStatus.APPROVED,
                description="Interest On Loan"
            )
            #Update loan interest and interest amount
            loan.interest_rate = interest
            loan.interest_amount = interest_amount

            # Apply and record charges
            add_charges(loan, 'Active')

            loan.status = LoanStatus.objects.get(name='Active')
            loan.save()
    except IntegrityError as e:        
        print(f"Disbursement failed for Loan ID {loan.id}: {str(e)}")
        loan.status = LoanStatus.objects.get(name='Failed')
        loan.save()

def add_charges(loan, next_status):
    """Add charges based on loan status."""
    charges = Charge.objects.filter(
        loan_status=LoanStatus.objects.get(name=next_status),
        mode='auto',
        is_active=True
    )
    for charge in charges:
        charge_amount = calculate_charge(loan.amount, charge) if charge.charge_application == 'principal' else calculate_charge(loan.balance, charge)
        if charge.charge_type == 'debit':
            LoanTransaction.objects.create(
                loan=loan,
                transaction_type=LoanTransaction.TransactionType.CHARGE,
                debit=charge_amount,
                currency=loan.currency,
                branch=loan.branch,
                status=LoanTransaction.TransactionStatus.APPROVED,
                description=charge.name
            )
        elif charge.charge_type == 'credit':
            LoanTransaction.objects.create(
                loan=loan,
                transaction_type=LoanTransaction.TransactionType.CHARGE,
                credit=charge_amount,
                currency=loan.currency,
                branch=loan.branch,
                status=LoanTransaction.TransactionStatus.APPROVED,
                description=charge.name
            )

def calculate_charge(loan_amount, charge):
    """Calculate charge amount."""
    if charge.amount_type == 'fixed':
        return charge.amount
    elif charge.amount_type == 'percentage':
        return (loan_amount * charge.amount / 100).quantize(Decimal('.01'))
    return Decimal('0.00')
