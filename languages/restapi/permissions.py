from rest_framework.permissions import BasePermission


class IsRegistered(BasePermission):
    """Checks whether student exists in Lesson object"""
    def has_object_permission(self, request, view, obj):
        return obj.student.filter(id=request.user.id).exists()