from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from apps.branch_assets.permissions import CanAddBranchAsset

from core.permissions import  BelongsToSameBranch, IsOwner
from .models import BranchAssets
from .serializers import BranchAssetSerializer

class BranchAssetsListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, CanAddBranchAsset ]
    queryset = BranchAssets.objects.all()
    serializer_class = BranchAssetSerializer    

    def create(self, request, *args, **kwargs):     
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class BranchAssetsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BranchAssets.objects.all()
    serializer_class = BranchAssetSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, BelongsToSameBranch]
