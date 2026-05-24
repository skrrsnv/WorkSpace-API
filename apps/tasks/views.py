from rest_framework import generics
from .serializer import TaskSerializer
from .models import Task
from apps.projects.models import Project
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .permissions import TaskActionPermission
from apps.projects.permissions import IsProjectMember
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.activity_logs.tasks import create_activity_log


class TaskListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

class TaskListCreate(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    pagination_class = TaskListPagination
    permission_classes = [IsAuthenticated, TaskActionPermission, IsProjectMember]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'priority', 'assignee']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date']
    ordering = ['-created_at']
    
    
    def get_queryset(self):
        return Task.objects.filter(project_id = self.kwargs['project_id'], project__memberships__user=self.request.user)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        context['project'] = project
        return context
    
    def perform_create(self, serializer):
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, id=project_id, memberships__user=self.request.user)
        task = serializer.save(project=project)
        
        create_activity_log.delay(self.request.user.id,
            "CREATE_TASK",
            {
                "task_id": task.id,
                "task_title": task.title,
                "project_id": project.id,
                "project_title": project.title
            })
    
    
class TaskRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, TaskActionPermission, IsProjectMember]
    
    def get_queryset(self):
        return Task.objects.filter(project_id = self.kwargs['project_id'], project__memberships__user=self.request.user)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        context['project'] = project
        return context
    
    def perform_update(self, serializer):
        task = serializer.save()
        create_activity_log.delay(self.request.user.id,
            "UPDATE_TASK",
            {
                "task_id": task.id,
                "task_title": task.title,
                "project_id": task.project.id,
                "project_title": task.project.title
            })
        
    def perform_destroy(self, instance):
        task_title = instance.title
        task_id = instance.id
        project_id = instance.project.id
        project_title = instance.project.title
        instance.delete()

        create_activity_log.delay(self.request.user.id,
            "DELETE_TASK",
            {
                "task_id": task_id,
                "task_title": task_title,
                "project_id": project_id,
                "project_title": project_title
            })