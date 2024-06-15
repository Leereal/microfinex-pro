from rest_framework import generics
from .models import Group
from .serializers import GroupSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from apps.groups import models

class AllGroupListView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class GroupListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        This view returns a list of all the groups for the currently authenticated user's active branch,
        including groups with no associated branch.
        """
        user = self.request.user
        if user.is_superuser:
            return Group.objects.all()  # Superuser can see all groups
        return Group.objects.filter(models.Q(branch=user.active_branch) | models.Q(branch__isnull=True))
    
    def perform_create(self, serializer):
        """
        Override this method to save the currently logged-in user as the creator of the group.
        """
        serializer.save(created_by=self.request.user)

class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        This view allows for retrieving, updating, or deleting a group
        based on the currently authenticated user's active branch.
        Groups with no associated branch are accessible by all users.
        """
        user = self.request.user
        if user.is_superuser:
            return Group.objects.all()  # Superuser can see all groups
        return Group.objects.filter(models.Q(branch=user.active_branch) | models.Q(branch__isnull=True))
