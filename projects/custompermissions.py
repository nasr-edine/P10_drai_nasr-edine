from rest_framework import permissions
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from projects.models import Project


# class ReadOnlyForContributors(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         print(obj)
#         print('False')
#         return False


class ReadOnlyForContributors(BasePermission):
    def has_permission(self, request, view):
        contributor = Project.objects.filter(
            contributors=request.user)
        print(contributor)

        print("True")
        return True


class ReadAndWriteOnly(BasePermission):
    def has_permission(self, request, view):
        print("True")
        return True


class ReadOnly(BasePermission):
    def has_permission(self, request, view):

        return request.method in SAFE_METHODS


class WriteOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return False
        else:
            return True

# class IsProjectContributorReadUpdate(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         list_contributors = obj.contributors.all()
#         if request.user in list_contributors:

#             if request.method in SAFE_METHODS:
#                 # The method is a safe method
#                 return True
#             else:
#                 # The method isn't a safe method
#                 # Only owners are granted permissions for unsafe methods
#                 return obj.author_user_id == request.user


# class IsProjectCreatorReadUpdateDelete(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in SAFE_METHODS:
#             # The method is a safe method
#             return True
#         else:
#             # The method isn't a safe method
#             # Only owners are granted permissions for unsafe methods
#             return obj.author_user_id == request.user


# def has_object_permission(self, request, view, obj):
#     # Read permissions are allowed to any request for contributors,
#     # so we'll always allow GET, HEAD or OPTIONS requests.
#     contributors = User.objects.filter(project=obj)
#     creator = User.objects.filter(project=obj, contributor__role='creator')

#     if request.user == creator:
#         return True
#     elif request.method in permissions.SAFE_METHODS and request.user in contributors:
#         return True
#     return False
