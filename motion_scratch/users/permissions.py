from rest_framework import permissions


class IsReceiverOfFriendRequestOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # For admin superusers:
        if request.user.is_superuser:
            return True
        # Allows all users to SAFE_METHODS (GET and OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # If user requesting is receiver of object:
        if request.user == obj.receiver:
            return True
        else:
            return False



