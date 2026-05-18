from django.db import models
from apps.projects.models import Project
from django.conf import settings


class Task(models.Model):
    class StatusChoices(models.TextChoices):
        todo = "todo", "Todo"
        in_progress = "in_progress", "In_progress"
        done = "done", "Done"
    
    class PriorityChoices(models.TextChoices):
        low = "low", "Low"
        medium = "medium", "Medium"
        high = "high", "High"
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.todo)
    priority = models.CharField(max_length=20, choices=PriorityChoices.choices, default=PriorityChoices.medium)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    