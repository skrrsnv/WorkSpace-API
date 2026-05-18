from rest_framework import serializers
from .models import Project, Membership

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'owner',
            'created_at'
        ]

        read_only_fields = [
            'owner',
            'created_at'
        ]
        
        
class MembershipSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Membership
        fields = [
            'id',
            'user',
            'project',
            'role',
            'created_at'
        ]
        read_only_fields = [
            'project',
            'created_at'
        ]
        
    def validate_role(self, value):
        if value == Membership.RoleChoices.owner:
            raise serializers.ValidationError("You cannot assign owner role")
        return value