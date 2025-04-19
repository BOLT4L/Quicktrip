from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request,view):
        return request.user.user_type == 'a'
    

class IsSub(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 's'
    
class IsBranch(BasePermission):
     
     def has_object_permission(self, request, view, obj):
        return request.user.branch == obj.branch
