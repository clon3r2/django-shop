from rest_framework.permissions import BasePermission



# class UserCustomPerm(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.user.id == obj.id


class IsOwnerPermission(BasePermission):
    def has_permission(self, request, view): # address list
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj): # user detail
        return request.user == obj.customer.user or request.user == obj
    
class IsOwnerCartItemPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return  request.user == obj.cart.customer.user


class IsSuperUserPermission(BasePermission):
    def has_permission(self, request, view): # user list
        return request.user.is_superuser

    