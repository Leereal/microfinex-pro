from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import GlobalSettings
from .serializers import GlobalSettingsSerializer

class GlobalSettingsListCreateView(generics.ListCreateAPIView):
    queryset = GlobalSettings.objects.all()
    serializer_class = GlobalSettingsSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class GlobalSettingsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GlobalSettings.objects.all()
    serializer_class = GlobalSettingsSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
