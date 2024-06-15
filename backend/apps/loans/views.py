from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from apps.loan_statuses.models import LoanStatus
from apps.loan_transactions.models import LoanTransaction
from apps.loan_transactions.serializers import LoanTransactionSerializer
from .models import Loan
from .serializers import LoanSerializer
from rest_framework.response import Response

class AllLoansListView(generics.ListAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class LoanListCreateView(generics.ListCreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        This view should return a list of all loans
        for the currently authenticated user's active branch.
        """
        user = self.request.user
        return Loan.objects.filter(branch=user.active_branch)
    
    def perform_create(self, serializer):       
        serializer.save(created_by=self.request.user, branch=self.request.user.active_branch)


class LoanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        This view allows for retrieving, updating, or deleting a loan
        based on the currently authenticated user's active branch.
        """
        user = self.request.user
        return Loan.objects.filter(branch=user.active_branch)

class ManageLoanView(generics.UpdateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        This view allows for updating a loan
        based on the currently authenticated user's active branch.
        """
        user = self.request.user
        return Loan.objects.filter(branch=user.active_branch)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        action = request.data.get('action')

        if action == 'approve':
            instance.approved_by = request.user
            instance.status = LoanStatus.objects.get(name='Approved')
            message = 'Loan approved successfully'

        elif action == 'reject':
            instance.approved_by = request.user
            instance.status = LoanStatus.objects.get(name='Rejected')
            message = 'Loan rejected successfully'
            
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        
        instance.save()

        return Response({'message': message}, status=status.HTTP_200_OK)

class LoanPaymentView(generics.CreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        loan = self.get_object()
        amount = request.data.get('amount')

        if amount is None:
            return Response({'error': 'Amount is required'}, status=status.HTTP_400_BAD_REQUEST)

        if float(amount) <= 0:
            return Response({'error': 'Amount must be greater than zero'}, status=status.HTTP_400_BAD_REQUEST)

        # Perform payment logic here

        # Assuming payment logic is successful
        return Response({'message': 'Payment processed successfully'}, status=status.HTTP_200_OK)

class LoanPaymentsView(generics.ListAPIView):
    serializer_class = LoanTransactionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        This view returns all payments for a specific loan.
        """
        loan_id = self.kwargs.get('pk')
        return LoanTransaction.objects.filter(loan_id=loan_id)