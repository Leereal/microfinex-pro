from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from .models import Employer
from .serializers import EmployerSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class EmployerListView(ListAPIView):
    """
    Provides a read-only list of all employers.
    """
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class EmployerDetailView(APIView):
    """
    Retrieve a single employer instance.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]    

    def get(self, request, pk, format=None):
        try:
            employer = Employer.objects.get(pk=pk)
            serializer = EmployerSerializer(employer)
            return Response(serializer.data)
        except Employer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
