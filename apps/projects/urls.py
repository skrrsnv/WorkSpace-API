from django.urls import path
from .views import ProjectListCreate, ProjectRetrieveUpdateDestroy, MembershipListCreate, MembershipRetrieveUpdateDestroy

urlpatterns = [
    path('', ProjectListCreate.as_view()),
    path('<int:pk>/', ProjectRetrieveUpdateDestroy.as_view()),
    path('<int:project_id>/membership/', MembershipListCreate.as_view()),
    path('<int:project_id>/membership/<int:pk>/', MembershipRetrieveUpdateDestroy.as_view()),
]