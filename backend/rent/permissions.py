from rest_framework import permissions 


class IsRenter(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user and request.user.is_authenticated and obj.account.user == request.user)
class IsRenterOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and (request.user == obj.account.user or request.user == obj.transport.owner.user)
    