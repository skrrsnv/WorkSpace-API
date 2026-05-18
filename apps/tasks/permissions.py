from rest_framework import permissions
from apps.projects.models import Membership

class TaskActionPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        
        if request.method == 'POST':
            project_id = view.kwargs.get('project_id')
            return Membership.objects.filter(project_id=project_id, user=request.user).exists()
        return True
    
    
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