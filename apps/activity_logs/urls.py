from django.urls import path
from .views import ActivityLogsView, ActivityLogsDetail

urlpatterns = [
    path('', ActivityLogsView.as_view()),
    path('<int:pk>/', ActivityLogsDetail.as_view())
]
