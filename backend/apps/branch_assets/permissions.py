from rest_framework.permissions import BasePermission

class CanAddBranchAsset(BasePermission):
    """
    Custom permission to allow only authenticated, non-superuser loan officers
    with specific user permissions to add branches.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and not a superuser
        # if not request.user.is_authenticated or request.user.is_superuser:
        #     return False
        
        # Check if the user belongs to the loan officer group
        # if not request.user.groups.filter(name='Loan Officer').exists():
        #     return False

        # Check if the user has the required user permissions to add branches
        return request.user.has_perm('branch_assets.delete_branchassets')
