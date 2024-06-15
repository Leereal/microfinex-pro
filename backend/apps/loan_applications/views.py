import re
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import LoanApplication, RejectionReason
from .serializers import LoanApplicationSerializer, RejectionReasonSerializer

User = get_user_model()

class AllLoanApplicationsListView(generics.ListAPIView):
    queryset = LoanApplication.objects.all()
    serializer_class = LoanApplicationSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class LoanApplicationListView(generics.ListCreateAPIView):
    serializer_class = LoanApplicationSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        This view should return a list of all loan applications
        for the currently authenticated user's active branch.
        """
        user = self.request.user
        return LoanApplication.objects.filter(branch=user.active_branch)

    def perform_create(self, serializer):
        """
        Ensure that the loan application is saved with the correct user and branch
        from the currently authenticated user's active branch.
        """
        serializer.save(user=self.request.user, branch=self.request.user.active_branch)

class LoanApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LoanApplicationSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        This view allows for retrieving, updating, or deleting a loan application
        based on the currently authenticated user's active branch.
        """
        user = self.request.user
        return LoanApplication.objects.filter(branch=user.active_branch)

class RejectionReasonListView(generics.ListCreateAPIView):
    queryset = RejectionReason.objects.all()
    serializer_class = RejectionReasonSerializer
    permission_classes = [IsAuthenticated]

class RejectionReasonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RejectionReason.objects.all()
    serializer_class = RejectionReasonSerializer
    permission_classes = [IsAuthenticated]
