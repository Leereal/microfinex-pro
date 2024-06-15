from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated,IsAdminUser, DjangoModelPermissions
from rest_framework.response import Response

from core.permissions import IsSuperuser

from .models import Branch
from .serializers import BranchSerializer

class BranchListAPIView(generics.ListCreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsSuperuser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class BranchDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsSuperuser]   
