from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import LoanStatus
from .serializers import LoanStatusSerializer

class LoanStatusListCreateView(generics.ListCreateAPIView):
    """
    API endpoint that allows loan statuses to be viewed or created.
    """
    queryset = LoanStatus.objects.all()
    serializer_class = LoanStatusSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class LoanStatusDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows a loan status to be retrieved, updated or deleted.
    """
    queryset = LoanStatus.objects.all()
    serializer_class = LoanStatusSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        Optionally restricts the queryset by filtering against a condition.
        Here, as an example, you could filter the queryset to only include loan statuses that are active or relevant to the user.
        """
        queryset = super().get_queryset()
        return queryset.filter(is_active=True)  # Example: return only active loan statuses
