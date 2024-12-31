from rest_framework.permissions import BasePermission

class IsAuthenticatedOrPostOnly(BasePermission):


    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user and request.user.is_authenticated
