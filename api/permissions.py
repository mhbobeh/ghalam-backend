from rest_framework.permissions import BasePermission


SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsOwnerOrReadOnly(BasePermission):
    """
    The request is as a owner, or is a read-only request.
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            return bool(
                request.user and
                request.user.is_authenticated
            )
            
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            request.user == obj.author
        )
