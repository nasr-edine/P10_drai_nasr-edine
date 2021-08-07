from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from issues.models import Comment, Issue
from issues.serializers import CommentSerializer, ProjectIssuesSerializer
from projects.custompermissions import (
    IsContributor, IsCreatorCommentOrReadOnlyForContributor,
    IsCreatorIssueOrReadOnlyForContributor)
from projects.models import Contributor, Project


class ProjectIssuesList(generics.ListCreateAPIView):
    """
    List all issues for a given project, or create a new issue.
    """
    serializer_class = ProjectIssuesSerializer
    permission_classes = [IsAuthenticated, IsContributor]

    def get_queryset(self):
        return Issue.objects.prefetch_related('project').filter(project__pk=self.kwargs.get('pk_project'))

    def create(self, request, pk_project, format=None):
        project = get_object_or_404(Project, pk=pk_project)
        serializer = ProjectIssuesSerializer(data=request.data, context={'project_id': pk_project})

        if not serializer.is_valid():
            return Response(serializer.errors)
        issue = serializer.save(author=request.user, project=project)
        return Response(ProjectIssuesSerializer(issue).data)


class ProjectIssuesDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a single issue.
    """
    serializer_class = ProjectIssuesSerializer
    permission_classes = [IsAuthenticated,
                          IsCreatorIssueOrReadOnlyForContributor]

    def get_queryset(self):
        try:
            project = Project.objects.get(pk=self.kwargs.get('pk_project'))
        except Project.DoesNotExist:
            raise Http404
        try:
            project.issues.get(pk=self.kwargs.get('pk'))
        except Issue.DoesNotExist:
            raise Http404
        queryset = Issue.objects.filter(project=project)
        return queryset


class CommentList(generics.ListCreateAPIView):
    """
    List all comments for a given project, or create a new comment.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsContributor]

    def get_queryset(self):
        try:
            project = Project.objects.get(pk=self.kwargs.get('pk_project'))
        except Project.DoesNotExist:
            raise Http404
        try:
            issue = project.issues.get(pk=self.kwargs.get('pk_issue'))
        except Issue.DoesNotExist:
            raise Http404
        comments = issue.comments.all()
        return comments

    def create(self, request, pk_project, pk_issue, format=None):
        project = get_object_or_404(Project, pk=pk_project)
        try:
            issue = project.issues.get(pk=pk_issue)
        except Issue.DoesNotExist:
            raise Http404
        serializer = CommentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        comment = serializer.save(author_id=request.user, issue_id=issue)
        return Response(CommentSerializer(comment).data)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a single comment.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated,
                          IsCreatorCommentOrReadOnlyForContributor]

    def get_queryset(self):
        try:
            project = Project.objects.get(pk=self.kwargs.get('pk_project'))
        except Project.DoesNotExist:
            raise Http404
        try:
            issue = project.issues.get(pk=self.kwargs.get('pk_issue'))
        except Issue.DoesNotExist:
            raise Http404
        try:
            issue.comments.get(pk=self.kwargs.get('pk'))
        except Comment.DoesNotExist:
            raise Http404
        return Comment.objects.filter(pk=self.kwargs.get('pk'))
