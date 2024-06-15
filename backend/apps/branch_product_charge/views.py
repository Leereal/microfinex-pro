from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.serializers import ValidationError

from apps.branch_product_charge.models import BranchProductCharge
from apps.branch_product_charge.serializers import BranchProductChargeSerializer

# Assuming BranchProductChargeSerializer is defined appropriately as shown earlier

class AllBranchProductChargesListView(generics.ListAPIView):
    queryset = BranchProductCharge.objects.all()
    serializer_class = BranchProductChargeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class BranchProductChargeListCreateView(generics.ListCreateAPIView):
    serializer_class = BranchProductChargeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        This view returns a list of all branch product charges for the currently authenticated user's active branch.
        """
        user = self.request.user
        return BranchProductCharge.objects.filter(branch_product__branch=user.active_branch)

    def perform_create(self, serializer):
        user = self.request.user
        branch_product = serializer.validated_data['branch_product']
        # Ensure the branch_product is part of the user's active branch before saving
        if branch_product.branch != user.active_branch:
            raise ValidationError("You can only add charges to products in your active branch.")
        serializer.save()

class BranchProductChargeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BranchProductChargeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        This view allows for retrieving, updating, or deleting a branch product charge based on the currently authenticated user's active branch.
        """
        user = self.request.user
        return BranchProductCharge.objects.filter(branch_product__branch=user.active_branch)
