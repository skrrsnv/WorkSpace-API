from rest_framework import generics
from .models import ActivityLog
from .serializer import ActivityLogSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class ActivityLogsView(generics.ListAPIView):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
  
class ActivityLogsDetail(generics.RetrieveAPIView):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer  
    permission_classes = [IsAdminUser, IsAuthenticated]