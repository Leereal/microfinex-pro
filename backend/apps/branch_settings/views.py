from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import BranchSettings
from .serializers import BranchSettingsSerializer

class BranchSettingsListCreateView(generics.ListCreateAPIView):
    queryset = BranchSettings.objects.all()
    serializer_class = BranchSettingsSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class BranchSettingsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BranchSettings.objects.all()
    serializer_class = BranchSettingsSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
