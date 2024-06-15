from rest_framework.permissions import BasePermission

class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is a superuser
        if request.user.is_superuser:
            return True

        if request.user.is_authenticated:
            return obj.user == request.user
        return False
    
class BelongsToSameBranch(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is a superuser
        if request.user.is_superuser:
            return True
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # Check if branch is provided in the request data
        branch_id = request.data.get('branch')
        if branch_id is not None:
            # Check if the provided branch matches the user's active branch
            return request.user.active_branch_id == branch_id
        else:
            # If branch is not provided, return True
            return True

    def has_object_permission(self, request, view, obj):
        # Check if the user is a superuser
        if request.user.is_superuser:
            return True

        if request.user.is_authenticated:
            return obj.branch == request.user.active_branch
        return False

#TODO create functionality to check ip when disbursing, repaying and approving loans
#Check branch and global settings first
# class IsIpAllowed(BasePermission):
#     def has_permission(self, request, view):
#         # Check if the user is a superuser
#         if request.user.is_superuser:
#             return True
#         # Check if the user is authenticated
#         if not request.user.is_authenticated:
#             return False
        
#         #TODO check if global settings allow all IPs
                
#         # Check if the user's IP is allowed
#         if request.META['REMOTE_ADDR'] in request.user.allowed_ips:
#             return True
        
#         return False