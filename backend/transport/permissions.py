from rest_framework import permissions 


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user and obj.owner.user == request.user)

class IsAuthAndNotOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user and obj.owner.user != request.user)
    
class IsOwnerOrNotAllow(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user and obj.owner.user == request.user)
