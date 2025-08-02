from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the object.
        return obj.creator == request.user


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to access it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Only allow access to the owner of the object.
        return obj.creator == request.user


class IsOwnerOrReadOnlyForPublic(permissions.BasePermission):
    """
    Custom permission that allows:
    - Read access to public objects for any user
    - Read access to any object for the owner
    - Write access only to the owner
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for public objects
        if request.method in permissions.SAFE_METHODS:
            if hasattr(obj, 'is_public') and obj.is_public:
                return True
            # Allow owner to read their own objects regardless of public status
            return obj.creator == request.user
        
        # Write permissions are only allowed to the owner of the object.
        return obj.creator == request.user
