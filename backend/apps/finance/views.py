from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from apps.finance.models import Finance
from .serializers import FinanceSerializer

class AllFinanceListView(generics.ListAPIView):
    queryset = Finance.objects.all()
    serializer_class = FinanceSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class FinanceListView(generics.ListCreateAPIView):
    queryset = Finance.objects.all()
    serializer_class = FinanceSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        This view should return a list of all finance
        for the currently authenticated user's active branch.
        """
        user = self.request.user
        return Finance.objects.filter(branch=user.active_branch)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, branch=self.request.user.active_branch)

class FinanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FinanceSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        This view allows for retrieving, updating, or deleting a finance
        based on the currently authenticated user's active branch.
        """
        user = self.request.user
        return Finance.objects.filter(branch=user.active_branch)
