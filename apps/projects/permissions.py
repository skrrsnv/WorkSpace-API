from rest_framework import permissions
from .models import Membership


class IsProjectMember(permissions.BasePermission):
    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_id')
        return Membership.objects.filter(project_id=project_id, user=request.user).exists()

        
class ProjectActionPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        membership = Membership.objects.filter(project=obj, user=request.user).first()

        if not membership:
            return False

        role = membership.role

        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.method in ['PUT', 'PATCH']:
            return role in [
                Membership.RoleChoices.owner,
                Membership.RoleChoices.admin
            ]

        if request.method == 'DELETE':
            return role == Membership.RoleChoices.owner

        return False
    
    
class MembershipActionPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        membership = Membership.objects.filter(project=obj.project, user=request.user).first()

        if not membership:
            return False

        role = membership.role

        if request.method in permissions.SAFE_METHODS:
            return True
 
        if request.method in ['PUT', 'PATCH']:
            return role in [
                Membership.RoleChoices.owner,
                Membership.RoleChoices.admin
            ]
      
        if request.method == 'DELETE':
            return role == Membership.RoleChoices.owner

        return False
    