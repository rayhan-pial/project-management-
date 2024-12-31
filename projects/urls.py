from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ProjectViewSet, TaskViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')

router.register(r'projects/(?P<project_id>[^/.]+)/tasks', TaskViewSet, basename='project-tasks')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('tasks/<int:task_id>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('api/', include(router.urls)),
]
