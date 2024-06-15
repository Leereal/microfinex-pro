import datetime
from decimal import Decimal
from django.utils import timezone
from django.db import transaction
from apps.charges.models import Charge
from apps.loan_statuses.models import LoanStatus
from apps.loans.models import Loan
from apps.loan_transactions.models import LoanTransaction
from dateutil.relativedelta import relativedelta

def short_term_calculation():
    # Get loans that need status checks
    loans = Loan.objects.filter(
        status__allow_auto_calculations=True,
        status__is_active=True
    )

    for loan in loans:
        #Grace period we take it from either group_product else branch_product
        grace_period_delta = datetime.timedelta(days=loan.branch_product.grace_period_days)
        # We use next_due_date if not the first time or expected_repayment_date if it is the first time
        target_date = loan.next_due_date or loan.expected_repayment_date
        target_date += grace_period_delta
        

        if timezone.now() > target_date:    
            with transaction.atomic():  
                
                duration_unit = loan.group_product.period.duration_unit if loan.group_product else loan.branch_product.period.duration_unit
                max_period = loan.group_product.max_period if loan.group_product else loan.branch_product.max_period
                min_period = loan.group_product.min_period if loan.group_product else loan.branch_product.min_period
                if duration_unit == 'days':
                    max_period_delta = datetime.timedelta(days=max_period)
                    period_delta = datetime.timedelta(days=min_period)
                    
                elif duration_unit == 'weeks':
                    max_period_delta = datetime.timedelta(weeks=max_period)
                    period_delta = datetime.timedelta(weeks=min_period)

                elif duration_unit == 'months':
                    max_period_delta = relativedelta(months=max_period)
                    period_delta = relativedelta(months=min_period)

                elif duration_unit == 'years':
                    max_period_delta = relativedelta(years=max_period)
                    period_delta = relativedelta(years=min_period)

                #Calculate final due date before moving to overdue
                final_due_date = loan.start_date + max_period_delta + grace_period_delta

                if timezone.now() > final_due_date:
                    loan.status = LoanStatus.objects.get(name="Overdue")
                    add_charges(loan, 'Overdue')
                else:                                  
                    if loan.status.name == "Active":
                        loan.status = LoanStatus.objects.get(name="Default")
                        loan.next_due_date = loan.expected_repayment_date + period_delta
                    else:
                        loan.next_due_date += period_delta

                    #Do the following if the loan was not added to overdue
                            
                    # Recalculate interest
                    interest = (loan.interest_rate / 100) * loan.balance
                    loan.interest_amount += interest

                    # Add the interest to loan_transactions
                    LoanTransaction.objects.create(
                        loan=loan,
                        transaction_type=LoanTransaction.TransactionType.INTEREST,
                        debit=interest,
                        currency=loan.currency,
                        branch=loan.branch,
                        status=LoanTransaction.TransactionStatus.APPROVED,
                        description="Interest on Balance"
                    )

                    #Add Charges based on loan status
                    add_charges(loan, loan.status.name)

                    loan.save()

def calculate_charge(loan_amount, charge):
    if charge.charge.amount_type == 'fixed':
        return charge.charge.amount
    elif charge.charge.amount_type == 'percentage':
        return (loan_amount * charge.charge.amount / 100).quantize(Decimal('.01'))
    return Decimal('0.00')

def add_charges(loan, next_status):
    # Add charges based on loan status    
    charges = Charge.objects.filter(loan_status=LoanStatus.objects.get(name=next_status), mode='auto', is_active=True)
    for charge in charges:
        # Apply charges
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

if __name__ == "__main__":
    short_term_calculation()
