from rest_framework import permissions
from projects.models import Contributor


class IsCreatorOrReadOnlyForContributor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            test = Contributor.objects.get(user=request.user, project=obj)
        except Contributor.DoesNotExist:
            print("You are not because you are not a contributor in this project")
            return False

        if request.method in permissions.SAFE_METHODS:
            print("You are access in read only because you're contributor")
            return True

        # Write permissions are only allowed to the creator of the project.
        try:
            test = Contributor.objects.get(
                user=request.user, project=obj, role='creator')
            print("You are access because you're the creator")
            return True
        except Contributor.DoesNotExist:
            print(
                "You are not access in Write because you're a contributor but not a creator")
            return False
