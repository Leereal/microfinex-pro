import datetime
from decimal import Decimal
from django.utils import timezone
from django.db import transaction
from dateutil.relativedelta import relativedelta
from apps.charges.models import Charge
from apps.loan_statuses.models import LoanStatus
from apps.loans.models import Loan
from apps.loan_transactions.models import LoanTransaction


def get_duration_delta(duration, duration_unit):
    """Get timedelta based on duration and duration unit."""
    if duration_unit == 'days':
        return datetime.timedelta(days=duration)
    elif duration_unit == 'weeks':
        return datetime.timedelta(weeks=duration)
    elif duration_unit == 'months':
        return relativedelta(months=duration)
    elif duration_unit == 'years':
        return relativedelta(years=duration)
    else:
        return datetime.timedelta()


def calculate_due_date(start_date, max_period_delta, grace_period_delta):
    """Calculate the final due date."""
    return start_date + max_period_delta + grace_period_delta


def add_interest_transaction(loan, interest):
    """Add interest transaction to loan."""
    return LoanTransaction.objects.create(
        loan=loan,
        transaction_type=LoanTransaction.TransactionType.INTEREST,
        debit=interest,
        currency=loan.currency,
        branch=loan.branch,
        status=LoanTransaction.TransactionStatus.APPROVED,
        description="Interest on Balance"
    )


def add_charges(loan, next_status):
    """Add charges based on loan status."""
    charges = Charge.objects.filter(
        loan_status=LoanStatus.objects.get(name=next_status),
        mode='auto',
        is_active=True
    )
    #This balance does not include current calculations
    # TODO make sure to calculate the charges correctly because here it's not the right way 
    previous_balance = loan.balance
    
    for charge in charges:
        charge_amount = calculate_charge(loan.amount, charge) if charge.charge_application == 'principal' else calculate_charge(previous_balance, charge)
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


def short_term_calculation():
    """Perform short term loan calculation."""
    loans = Loan.objects.filter(
        status__allow_auto_calculations=True,
        status__is_active=True
    )

    for loan in loans:
        print("We have loan : ",loan)
        grace_period_delta = datetime.timedelta(days=loan.group_product.grace_period_days) if loan.group_product else datetime.timedelta(days=loan.branch_product.grace_period_days)
        print("Grace Period : ", grace_period_delta)
        target_date = loan.next_due_date or loan.expected_repayment_date
        target_date += grace_period_delta

        print("Target Date : ", target_date)

        if timezone.now() > target_date:
            with transaction.atomic():
                duration_unit = loan.group_product.period.duration_unit if loan.group_product else loan.branch_product.period.duration_unit
                max_period = loan.group_product.max_period if loan.group_product else loan.branch_product.max_period
                min_period = loan.group_product.min_period if loan.group_product else loan.branch_product.min_period
                
                max_period_delta = get_duration_delta(max_period, duration_unit)
                period_delta = get_duration_delta(min_period, duration_unit)

                final_due_date = calculate_due_date(loan.start_date, max_period_delta, grace_period_delta)
                print("Final Due Date : ", final_due_date)

                if timezone.now() > final_due_date:
                    loan.status = LoanStatus.objects.get(name="Overdue")
                    add_charges(loan, 'Overdue')
                else:
                    if loan.status.name == "Active":
                        loan.status = LoanStatus.objects.get(name="Default")
                        loan.next_due_date = loan.expected_repayment_date + period_delta
                        print("Next Due Date : ", loan.next_due_date)
                    else:
                        loan.next_due_date += period_delta
                        print("Else Next Due Date : ", loan.next_due_date)

                    interest = (loan.interest_rate / 100) * loan.balance
                    loan.interest_amount += interest
                    print("Interest : ", interest)
                    add_interest_transaction(loan, interest)
                    add_charges(loan, loan.status.name)

                    loan.save()


if __name__ == "__main__":
    short_term_calculation()
