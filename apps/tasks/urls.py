from django.urls import path
from .views import TaskListCreate, TaskRetrieveUpdateDestroy

urlpatterns = [
    path('<int:project_id>/tasks/', TaskListCreate.as_view()),
    path('<int:project_id>/tasks/<int:pk>/', TaskRetrieveUpdateDestroy.as_view()),    
]
