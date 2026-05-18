from .models import Task
from rest_framework import serializers

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'project',
            'assignee',
            'created_at',
            'due_date'
        ]
        read_only_fields = [
            'project',
            'created_at'
        ]
        
    def validate_assignee(self, value):
        project = self.context['project']
        is_member = project.memberships.filter(user=value).exists()
            
        if not is_member:
            raise serializers.ValidationError("User is not project member")
        return value
    