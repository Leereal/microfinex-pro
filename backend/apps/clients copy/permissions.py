from rest_framework import permissions

class IsUserFromBranch(permissions.BasePermission):
    """
    Custom permission to only allow users associated with the branch to access the client.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is associated with any branch that matches the client's branch
        user = request.user
        client_branch = obj.branch
        user_branches = user.branches.all()

        return client_branch in user_branches
