from rest_framework import permissions


class IsProjectContributorReadUpdate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        list_contributors = obj.contributors.all()
        if request.user in list_contributors:

            if request.method in permissions.SAFE_METHODS:
                # The method is a safe method
                return True
            else:
                # The method isn't a safe method
                # Only owners are granted permissions for unsafe methods
                return obj.author_user_id == request.user


class IsProjectCreatorReadUpdateDelete(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # The method is a safe method
            return True
        else:
            # The method isn't a safe method
            # Only owners are granted permissions for unsafe methods
            return obj.author_user_id == request.user