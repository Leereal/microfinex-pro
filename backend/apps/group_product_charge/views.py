from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from apps.group_product_charge.models import GroupProductCharge
from apps.group_product_charge.serializers import GroupProductChargeSerializer
from rest_framework.serializers import ValidationError

class AllGroupProductChargesListView(generics.ListAPIView):
    queryset = GroupProductCharge.objects.all()
    serializer_class = GroupProductChargeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class GroupProductChargeListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupProductChargeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        Return a list of all group product charges for the currently authenticated user's active branch.
        """
        user = self.request.user
        return GroupProductCharge.objects.filter(group_product__group__branch=user.active_branch)

    def perform_create(self, serializer):
        user = self.request.user
        group_product = serializer.validated_data['group_product']
        # Ensure the group_product is part of the user's active branch before saving
        if group_product.branch != user.active_branch:
            raise ValidationError("You can only add charges to group products in your active branch.")
        serializer.save()

class GroupProductChargeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupProductChargeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        Allows retrieving, updating, or deleting a group product charge based on the currently authenticated user's active branch.
        """
        user = self.request.user
        return GroupProductCharge.objects.filter(group_product__group__branch=user.active_branch)
