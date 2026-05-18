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
        serializer.save(project=project)
    
    
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
    