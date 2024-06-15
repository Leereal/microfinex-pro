from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Charge
from .serializers import ChargeSerializer

class ChargeListCreateView(generics.ListCreateAPIView):
    queryset = Charge.objects.all()
    serializer_class = ChargeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class ChargeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Charge.objects.all()
    serializer_class = ChargeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
