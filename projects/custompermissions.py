from issues.models import Comment, Issue
from rest_framework import permissions
from projects.models import Contributor
from projects.models import Project
from django.http import Http404


class IsCreatorOrReadOnlyForContributor(permissions.BasePermission):

    def has_permission(self, request, view):
        pk = request.resolver_match.kwargs.get('pk')
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404
        try:
            Contributor.objects.get(user=request.user, project=project)
        except Contributor.DoesNotExist:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            Contributor.objects.get(
                user=request.user, project=project, role='creator')
            return True
        except Contributor.DoesNotExist:
            return False


class IsContributor(permissions.BasePermission):

    def has_permission(self, request, view):
        pk = request.resolver_match.kwargs.get('pk_project')
        try:
            project = Project.objects.get(pk=pk)
            print(project)
        except Project.DoesNotExist:
            print('Project.DoesNotExist')
            raise Http404
        try:
            Contributor.objects.get(user=request.user, project=project)
            return True
        except Contributor.DoesNotExist:
            return False


class IsCreatorIssueOrReadOnlyForContributor(permissions.BasePermission):

    def has_permission(self, request, view):
        pk = request.resolver_match.kwargs.get('pk_project')
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404
        try:
            Contributor.objects.get(user=request.user, project=project)
        except Contributor.DoesNotExist:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            issue = project.issues.get(
                pk=request.resolver_match.kwargs.get('pk'))
        except Issue.DoesNotExist:
            raise Http404
        try:
            issue = project.issues.get(
                pk=request.resolver_match.kwargs.get('pk'), author=request.user)
            return True
        except Issue.DoesNotExist:
            return False


class IsCreatorCommentOrReadOnlyForContributor(permissions.BasePermission):

    def has_permission(self, request, view):
        print('IsCreatorCommentOrReadOnlyForContributor called')
        pk = request.resolver_match.kwargs.get('pk_project')
        try:
            project = Project.objects.get(pk=pk)
            print(project)
        except Project.DoesNotExist:
            raise Http404
        try:
            contributor = Contributor.objects.get(
                user=request.user, project=project)
            print(contributor)
        except Contributor.DoesNotExist:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            issue = project.issues.get(
                pk=request.resolver_match.kwargs.get('pk_issue'))
            print(issue)
        except Issue.DoesNotExist:
            raise Http404
        try:
            comment = issue.comments.get(
                pk=request.resolver_match.kwargs.get('pk'))
            print(comment)
        except Comment.DoesNotExist:
            raise Http404
        try:
            comment = issue.comments.get(
                pk=request.resolver_match.kwargs.get('pk'), author_id=request.user)
            print(comment)
            return True

        except Comment.DoesNotExist:
            return False
