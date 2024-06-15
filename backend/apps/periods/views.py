from rest_framework import generics
from .models import Period
from .serializers import PeriodSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class PeriodListCreateView(generics.ListCreateAPIView):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer
    permission_classes = [IsAuthenticated, IsAdminUser] 

class PeriodDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Period.objects.all()
    serializer_class = [IsAuthenticated, IsAdminUser] 
