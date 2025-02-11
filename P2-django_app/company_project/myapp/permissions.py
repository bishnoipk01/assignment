from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to modify objects.
    Anyone (including non-admins) can read (GET, HEAD, OPTIONS).
    """

    def has_permission(self, request, view):
        # Allow read-only methods for any request.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to admin (staff) users.
        return request.user and request.user.is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit or delete it.
    Assumes the model instance has an 'id' attribute that can be compared to request.user.id.
    """

    def has_object_permission(self, request, view, obj):
        # Allow safe methods (GET, HEAD, OPTIONS) for any request.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Admin users can edit any data.
        if request.user.is_staff or request.user.is_superuser:
            return True


        # Allow write permissions only if the object's id matches the logged-in user's id.
        return obj.id == request.user.id