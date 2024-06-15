from rest_framework import generics
from .models import GroupProduct
from .serializers import GroupProductSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q

class AllGroupProductListView(generics.ListAPIView):
    queryset = GroupProduct.objects.all()
    serializer_class = GroupProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class GroupProductListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
            """
            This view returns a list of all the group products for the currently authenticated user's active branch,
            including group products from groups with no associated branch.
            """
            user = self.request.user
            # Filter for group products where the group is in the user's active branch or the group has no branch
            return GroupProduct.objects.filter(Q(group__branch=user.active_branch) | Q(group__branch__isnull=True))


class GroupProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        This view allows for retrieving, updating, or deleting a group product
        based on the currently authenticated user's active branch or for groups with no associated branch.
        """
        user = self.request.user
        # Filter for group products where the group is in the user's active branch or the group has no branch
        return GroupProduct.objects.filter(Q(group__branch=user.active_branch) | Q(group__branch__isnull=True))
