from rest_framework.permissions import BasePermission

class HaveBranch(BasePermission):
    """
    Check to see if the user has any branch assigned to them
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and not a superuser
        if not request.user.is_authenticated:
            return False

        # Check if the user has any branch assigned to them
        return request.user.user_branches.exists()
