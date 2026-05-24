from django.db import models
from django.conf import settings


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class Membership(models.Model):
    
    class RoleChoices(models.TextChoices):
        owner = 'owner', 'Owner'
        admin = 'admin', 'Admin'
        member = 'member', 'Member'
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=20, choices=RoleChoices.choices, default=RoleChoices.member)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Project: {self.project.title} | User: {self.user.username} | Role: {self.role}'
    
    class Meta:
        unique_together = ('project', 'user')
        