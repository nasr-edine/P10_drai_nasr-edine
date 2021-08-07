from django.http import Http404
from rest_framework import permissions

from issues.models import Comment, Issue
from projects.models import Contributor, Project


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
            (project)
        except Project.DoesNotExist:
            ('Project.DoesNotExist')
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
            project.issues.get(
                pk=request.resolver_match.kwargs.get('pk'))
        except Issue.DoesNotExist:
            raise Http404
        try:
            project.issues.get(
                pk=request.resolver_match.kwargs.get('pk'), author=request.user)
            return True
        except Issue.DoesNotExist:
            return False


class IsCreatorCommentOrReadOnlyForContributor(permissions.BasePermission):

    def has_permission(self, request, view):
        ('IsCreatorCommentOrReadOnlyForContributor called')
        pk = request.resolver_match.kwargs.get('pk_project')
        try:
            project = Project.objects.get(pk=pk)
            (project)
        except Project.DoesNotExist:
            raise Http404
        try:
            contributor = Contributor.objects.get(
                user=request.user, project=project)
            (contributor)
        except Contributor.DoesNotExist:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            issue = project.issues.get(
                pk=request.resolver_match.kwargs.get('pk_issue'))
            (issue)
        except Issue.DoesNotExist:
            raise Http404
        try:
            comment = issue.comments.get(
                pk=request.resolver_match.kwargs.get('pk'))
            (comment)
        except Comment.DoesNotExist:
            raise Http404
        try:
            comment = issue.comments.get(
                pk=request.resolver_match.kwargs.get('pk'), author_id=request.user)
            (comment)
            return True

        except Comment.DoesNotExist:
            return False
