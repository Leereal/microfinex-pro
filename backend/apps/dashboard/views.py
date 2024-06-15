from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from apps.clients.models import Client
from apps.finance.models import Finance
from apps.loan_transactions.models import LoanTransaction
from apps.loans.models import Loan
from apps.loans.serializers import LoanSerializer

class DashboardSummaryView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        #Fetch total clients we have
        total_clients = Client.objects.all().count()

        # Fetch total disbursements count
        total_disbursements = Loan.objects.all().count()
        
        # Fetch total payments count
        total_payments = LoanTransaction.objects.filter(transaction_type='repayment').count()
        
        # Fetch total disbursements amount
        total_disbursements_amount = LoanTransaction.objects.filter(transaction_type='disbursement').aggregate(Sum('debit'))['debit__sum'] or 0
        
        # Fetch total payments amount
        total_payments_amount = LoanTransaction.objects.filter(transaction_type='repayment').aggregate(Sum('credit'))['credit__sum'] or 0
        
        # Fetch total loans processed count
        total_loans_processed = LoanTransaction.objects.filter(transaction_type='disbursement').distinct('loan').count()
        
        # Fetch recent loans
        recent_loans = Loan.objects.all().order_by('-created_at')[:5]
        
        # Serialize recent loans using LoanSerializer
        recent_loans_data = LoanSerializer(recent_loans, many=True).data

        # Fetch new clients this week
        start_of_week = timezone.now() - timedelta(days=timezone.now().weekday())
        new_clients_this_week = Client.objects.filter(created_at__gte=start_of_week).count()
        
        # Calculate percentage increase in disbursements since last week
        start_of_last_week = start_of_week - timedelta(days=7)
        disbursements_last_week = LoanTransaction.objects.filter(
            transaction_type='disbursement',
            created_at__range=(start_of_last_week, start_of_week)
        ).aggregate(Sum('debit'))['debit__sum'] or 0
        
        percentage_increase_disbursements = ((total_disbursements_amount - disbursements_last_week) / disbursements_last_week) * 100 if disbursements_last_week else 0

        # Count number of last week LoanTransactions with credit value not none
        last_week_transactions_with_credit = LoanTransaction.objects.filter(
            transaction_type='repayment',
            created_at__range=(start_of_last_week, start_of_week),
            credit__isnull=False
        ).count()

        # Count number of Loans that have status = Rejected
        rejected_loans_count = Loan.objects.filter(status__name='Rejected').count()

        # Calculate available funds for a specific branch
        branch_id = request.user.active_branch
        available_funds = Finance.calculate_available_funds(branch_id)

        # Prepare summary data
        summary_data = {
            "total_clients": total_clients,
            'total_disbursements': total_disbursements,
            'total_payments': total_payments,
            'total_disbursements_amount': total_disbursements_amount,
            'total_payments_amount': total_payments_amount,
            'total_loans_processed': total_loans_processed,
            'recent_loans': recent_loans_data,
            'new_clients_this_week': new_clients_this_week,
            'percentage_increase_disbursements': percentage_increase_disbursements,
            'last_week_transactions_with_credit': last_week_transactions_with_credit,
            'rejected_loans_count': rejected_loans_count,
            'available_funds': available_funds
        }

        return Response(summary_data)
