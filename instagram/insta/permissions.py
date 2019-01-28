# from rest_framework.permissions import BasePermission
#
#
# class IsAllowedToEdit(BasePermission):
#
#     def has_permission(self, request, view):
#         return request.user.id == "Author"
from rest_framework import permissions
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        # if request.method in permissions.SAFE_METHODS:
        #     return True
        return obj.username == request.user.username

class IsPostOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        print(obj.user.id)
        print(request.user.id)
        return obj.user.id == request.user.id


