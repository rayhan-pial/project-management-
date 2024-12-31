from rest_framework.permissions import BasePermission

class IsProjectOwnerOrUser(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in ['GET', 'POST']:
            return True
        else:
            return obj.owner == request.user


class IsTaskOwnerOrUser(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.project.owner == request.user
        else:
            return (obj.project.owner == request.user or obj.assigned_to == request.user)


class IsCommentUserOrOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.user == request.user
        else:
            return (obj.user == request.user or obj.task.project.owner == request.user)

