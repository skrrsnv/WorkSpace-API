from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Project, Membership
from .serializer import ProjectSerializer, MembershipSerializer
from .permissions import MembershipActionPermission, ProjectActionPermission, IsProjectMember
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.activity_logs.tasks import create_activity_log


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
        
        create_activity_log.delay(self.request.user.id,
            "CREATE_PROJECT",
            {
                "project_id": project.id,
                "title": project.title,
                "owner_id": project.owner.id
            })
        
    
    
class ProjectRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectActionPermission]
    
    def get_queryset(self):
        return Project.objects.filter(memberships__user=self.request.user)
    
    def perform_update(self, serializer):
        project = serializer.save()
        create_activity_log.delay(self.request.user.id,
            "UPDATE_PROJECT",
            {
                "project_id": project.id,
                "title": project.title,
                "owner_id": project.owner.id
            })
        
    def perform_destroy(self, instance):
        title = instance.title
        project_id = instance.id
        owner_id = instance.owner.id
        instance.delete()

        create_activity_log.delay(self.request.user.id,
            "DELETE_PROJECT",
            {
                "project_id": project_id,
                "title": title,
                "owner_id": owner_id
            })
    

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
        membership = serializer.save(project=project)
        
        create_activity_log.delay(
            self.request.user.id,
            "ADD_MEMBER",
        {
            "membership_id": membership.id,
            "user_id": membership.user.id,
            "role": membership.role,
            "project_id": membership.project.id
        }
)
    
    
class MembershipRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated, MembershipActionPermission, IsProjectMember]
    
    def get_queryset(self):
        return Membership.objects.filter(project_id = self.kwargs['project_id'], project__memberships__user=self.request.user)
    
    def perform_update(self, serializer):
        membership = serializer.save()
        
        create_activity_log.delay(self.request.user.id, "UPDATE_MEMBER",
        {
            "membership_id": membership.id,
            "user_id": membership.user.id,
            "role": membership.role,
            "project_id": membership.project.id
        })
        
    def perform_destroy(self, instance):
        user_id = instance.user.id
        role = instance.role
        project_id = instance.project.id
        membership_id = instance.id
        
        instance.delete()

        create_activity_log.delay(self.request.user.id, "DELETE_MEMBER",
        {
            "membership_id": membership_id,
            "user_id": user_id,
            "role": role,
            "project_id": project_id
        })
    
