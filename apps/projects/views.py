from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Project, Membership
from .serializer import ProjectSerializer, MembershipSerializer
from .permissions import MembershipActionPermission, ProjectActionPermission, IsProjectMember
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


# Create your views here.

class ProjectListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class ProjectListCreate(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = ProjectListPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['owner']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    
    def get_queryset(self):
        return Project.objects.filter(memberships__user=self.request.user)
    
    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)
        Membership.objects.create(project=project, user=self.request.user, role=Membership.RoleChoices.owner)
        
    
    
class ProjectRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectActionPermission]
    
    def get_queryset(self):
        return Project.objects.filter(memberships__user=self.request.user)
    

class MembershipPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100    
    

class MembershipListCreate(generics.ListCreateAPIView):
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated, MembershipActionPermission, IsProjectMember]
    pagination_class = MembershipPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['role']
    search_fields = ['user__username', 'user__email']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    
    def get_queryset(self):
        return Membership.objects.filter(project_id = self.kwargs['project_id'], project__memberships__user=self.request.user)
    
    
    def perform_create(self, serializer):
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, id=project_id, memberships__user=self.request.user, memberships__role__in=[
            Membership.RoleChoices.owner, Membership.RoleChoices.admin])
        serializer.save(project=project)
    
    
class MembershipRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated, MembershipActionPermission, IsProjectMember]
    
    def get_queryset(self):
        return Membership.objects.filter(project_id = self.kwargs['project_id'], project__memberships__user=self.request.user)
    
