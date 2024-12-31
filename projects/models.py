from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProjectMember(models.Model):
    ROLE_CHOICES = [('Admin', 'Admin'), ('Member', 'Member')]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_user')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)


    def __str__(self):
        return f"{self.user.username} - {self.project.name}"


class Task(models.Model):
    STATUS_CHOICES = [('To Do', 'To Do'), ('In Progress', 'In Progress'), ('Done', 'Done')]
    PRIORITY_CHOICES = [('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='To Do')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='task_user')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='task_project')
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()

    def __str__(self):
        return f"{self.title} - {self.project.name} - {self.assigned_to}"


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comment_task')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.task.title}"
