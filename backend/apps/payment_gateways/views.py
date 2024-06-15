from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from apps.payment_gateways.models import PaymentGateway
from .serializers import PaymentGatewaySerializer

class PaymentGatewayListCreateView(generics.ListCreateAPIView):
    queryset = PaymentGateway.objects.all()
    serializer_class = PaymentGatewaySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class PaymentGatewayDetailView(generics.RetrieveUpdateDestroyAPIView):  
    queryset = PaymentGateway.objects.all()
    serializer_class = PaymentGatewaySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]