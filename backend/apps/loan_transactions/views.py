from rest_framework import generics, status
from rest_framework.response import Response
from .models import LoanTransaction
from .serializers import LoanTransactionSerializer
from apps.loans.models import Loan
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class AllTransactions(generics.ListAPIView):
    queryset = LoanTransaction.objects.all()
    serializer_class = LoanTransactionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    

class AddChargeView(generics.CreateAPIView):
    serializer_class = LoanTransactionSerializer
    queryset = LoanTransaction.objects.all()

    def post(self, request, *args, **kwargs):
        loan_id = request.data.pop('loan_id')  # Extract loan_id from request data
        loan = Loan.objects.get(pk=loan_id)    # Get the loan object
        request.data['loan'] = loan            # Add the loan object to request data
        request.data['transaction_type'] = LoanTransaction.TransactionType.CHARGE
        request.data['created_by'] = request.user
        request.data['branch'] = request.user.active_branch
        return self.create(request, *args, **kwargs)

class RefundView(generics.CreateAPIView):
    serializer_class = LoanTransactionSerializer
    queryset = LoanTransaction.objects.all()

    def post(self, request, *args, **kwargs):
        loan_id = request.data.pop('loan_id')  # Extract loan_id from request data
        loan = Loan.objects.get(pk=loan_id)    # Get the loan object
        request.data['loan'] = loan            # Add the loan object to request data
        request.data['transaction_type'] = LoanTransaction.TransactionType.REFUND
        request.data['created_by'] = request.user
        request.data['branch'] = request.user.active_branch
        return self.create(request, *args, **kwargs)

class BonusView(generics.CreateAPIView):
    serializer_class = LoanTransactionSerializer
    queryset = LoanTransaction.objects.all()

    def post(self, request, *args, **kwargs):
        loan_id = request.data.pop('loan_id')  # Extract loan_id from request data
        loan = Loan.objects.get(pk=loan_id)    # Get the loan object
        request.data['loan'] = loan            # Add the loan object to request data
        request.data['transaction_type'] = LoanTransaction.TransactionType.BONUS
        request.data['created_by'] = request.user
        request.data['branch'] = request.user.active_branch
        return self.create(request, *args, **kwargs)

class TopUpView(generics.CreateAPIView):
    serializer_class = LoanTransactionSerializer
    queryset = LoanTransaction.objects.all()

    def post(self, request, *args, **kwargs):
        loan_id = request.data.pop('loan_id')  # Extract loan_id from request data
        loan = Loan.objects.get(pk=loan_id)    # Get the loan object
        request.data['loan'] = loan            # Add the loan object to request data
        request.data['transaction_type'] = LoanTransaction.TransactionType.TOPUP
        request.data['created_by'] = request.user
        request.data['branch'] = request.user.active_branch
        return self.create(request, *args, **kwargs)
    
