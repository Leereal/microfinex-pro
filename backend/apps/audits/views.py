from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsSuperuser
from .models import AuditLog
from .serializers import AuditLogSerializer

class AuditLogListAPIView(generics.ListAPIView):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsSuperuser]

class AuditLogDetailAPIView(generics.RetrieveAPIView):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsSuperuser]
