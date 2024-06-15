from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from dj_rest_auth.views import LoginView
from apps.branches.models import Branch

from apps.users.permissions import HaveBranch
from core.permissions import IsSuperuser

from .models import User, UserBranch
from .serializers import UserBranchSerializer, UserSerializer

class CustomUserDetailsView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return get_user_model().objects.none()

class CustomUserEditView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # Restrict access to admin users

    def get_object(self):
        pk = self.kwargs.get('pk')
        return User.objects.get(pk=pk)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Updating user's branches if provided in the request
        branches_data = request.data.get('branches')    
        if branches_data:
            user_branches = instance.user_branches.all()
            user_branch_serializer = UserBranchSerializer(user_branches, data=branches_data, many=True)
            if user_branch_serializer.is_valid():
                user_branch_serializer.save()
                return Response(user_branch_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(user_branch_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # No branches data provided, return error
            return Response({"detail": "No branches data provided"}, status=status.HTTP_400_BAD_REQUEST)
        

class CustomLoginView(LoginView):
     # Override the post method to check if the user has branches before allowing login
    def post(self, request, *args, **kwargs):
        # Call parent's post method to perform the login
        response = super().post(request, *args, **kwargs)
        
        # Check if the login was successful
        if response.status_code == status.HTTP_200_OK:
            # If successful, check branch permissions
            if not HaveBranch().has_permission(request, self):
                # If the user doesn't have branches assigned, raise an exception
                raise AuthenticationFailed("You don't have any branches assigned.")
            else:
                # If the user has branches assigned, return the response
                return self.get_response()
        else:
            # If the login was not successful, return the response as is
            return response
    
    #I did this so that we return more data when user logged in
    def get_response(self):
        original_response = super().get_response()
        if original_response.status_code == status.HTTP_200_OK:
            user = self.user
            original_response.data["user"] = UserSerializer(user).data
            return original_response
        return original_response
    
class UserBranchView(CreateAPIView, DestroyAPIView):
    queryset = UserBranch.objects.all()
    serializer_class = UserBranchSerializer
    permission_classes = [IsSuperuser]

    def create(self, request, *args, **kwargs):
        assigner = request.user
        user_id = request.data.get("user")  # Accessing user_id from request.data
        branch_id = request.data.get("branch")
        user = get_object_or_404(User, id=user_id)
        branch = get_object_or_404(Branch, id=branch_id)

        if UserBranch.objects.filter(user=user, branch=branch).exists():
            return Response(
                {
                "detail":"User is already part of the branch"
                },
                status = status.HTTP_400_BAD_REQUEST
            )
        assignment = UserBranch.objects.create(user=user, branch=branch, created_by=assigner)
        assignment.save()

        return Response(
            {"detail":"User assigned to branch successfully"},
            status=status.HTTP_201_CREATED
        )
    
    def delete(self, request, *args, **kwargs):

        user_id = request.data.get("user")  # Accessing user_id from request.data
        branch_id = request.data.get("branch")
        user = get_object_or_404(User, id=user_id)
        branch = get_object_or_404(Branch, id=branch_id)

        assignment = get_object_or_404(UserBranch, user=user, branch=branch)
        assignment.delete()

        return Response(
            {"detail":"User removed from branch successfully"},
            status=status.HTTP_204_NO_CONTENT
        )




