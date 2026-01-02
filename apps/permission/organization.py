from typing import Any
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView
from apps.userprofile.models import UserProfile

class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role==UserProfile.ROLE_ADMIN)
    

class IsManager(BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role==UserProfile.ROLE_MANAGER)
    
class IsManagerOrAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in [UserProfile.ROLE_MANAGER, UserProfile.ROLE_ADMIN]
        )

class IsEmployee(BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role==User.ROLE_EMPLOYEE)
     

class IsAdminSameOrganization(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated and request.user.role==UserProfile.ROLE_ADMIN and request.user.organization==obj.organization )

class IsAdminOrManagerSameOrganization(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated and request.user.role in [UserProfile.ROLE_MANAGER, UserProfile.ROLE_ADMIN] and request.user.organization==obj.organization )
    

class CanModifyUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        user=request.user
        if not user.is_authenticated:
            return False
        
        if user.organization!=obj.organization:
            return False
        
        if user.role==UserProfile.ROLE_ADMIN:
            return True
        
        if user.role==UserProfile.ROLE_MANAGER:
            return obj.role==UserProfile.ROLE_EMPLOYEE
        
        return user.id==obj.id
   
class CanDeleteUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        user=request.user
        if not user.is_authenticated:
            return False
        
        if user.organization!=obj.organization:
            return False
        
        if user.role==UserProfile.ROLE_ADMIN:
            return True
        if obj.role==UserProfile.ROLE_EMPLOYEE and user.role==UserProfile.ROLE_MANAGER:
            return True
        
        return False
  