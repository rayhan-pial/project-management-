from rest_framework import viewsets, permissions
from .models import Project, Task, Comment
from .serializers import ProjectSerializer, TaskSerializer, CommentSerializer

from rest_framework.exceptions import PermissionDenied

from .customPermissions import IsProjectOwnerOrUser, IsTaskOwnerOrUser , IsCommentUserOrOwner


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectOwnerOrUser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsTaskOwnerOrUser]

    def get_queryset(self):

        project_id = self.kwargs.get('project_id')
        if project_id:
            project = Project.objects.filter(id=project_id).first()

            if not project:
                raise PermissionDenied("You do not have permission to access tasks for this project.")


        assigned_tasks = Task.objects.filter(assigned_to=self.request.user)

        owner_tasks = Task.objects.filter(project__owner=self.request.user)

        result_queryset = assigned_tasks | owner_tasks

        if project_id:
            result_queryset = result_queryset.filter(project_id=project_id)

        return result_queryset


    def perform_create(self, serializer):

        project_id = self.kwargs.get('project_id')
        project = Project.objects.filter(id=project_id, owner=self.request.user).first()

        if not project:
            raise PermissionDenied("You do not have permission to create a task in this project.")

        serializer.save(project=project)



class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommentUserOrOwner]

    def get_queryset(self):

        task_id = self.kwargs.get('task_id')
        if task_id:
            task = Task.objects.filter(id=task_id).first()

            if not task:
                raise PermissionDenied("You do not have permission to access tasks for this project.")

        user_comment = Comment.objects.filter(user=self.request.user)

        owner_tasks = Comment.objects.filter(task__project__owner=self.request.user)

        result_queryset = user_comment | owner_tasks

        if task_id:
            result_queryset = result_queryset.filter(task_id=task_id)

        return result_queryset

    def perform_create(self, serializer):
        task_id = self.kwargs.get('task_id')
        if task_id:
            task = Task.objects.select_related('project__owner', 'assigned_to').filter(id=task_id).first()

            if task and (task.project.owner == self.request.user or task.assigned_to == self.request.user):
                serializer.save(user=self.request.user, task=task)


        if not task_id:
            raise PermissionDenied("You do not have permission to create a task in this project.")
        serializer.save(user=self.request.user)

