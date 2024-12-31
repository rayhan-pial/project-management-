from rest_framework import serializers
from .models import Project, ProjectMember, Task, Comment

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'created_at']
        read_only_fields = ['owner']


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'assigned_to', 'project', 'created_at', 'due_date']


    def validate(self, data):

        user = self.context['request'].user
        project = data.get('project')

        if project and project.owner != user:
            raise serializers.ValidationError({"project": "You are not the owner of this project."})

        return data




class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'task', 'created_at']
        read_only_fields = ['user']
