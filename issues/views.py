from rest_framework.serializers import Serializer
from issues.models import Issue
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import ProtectedError

from projects.models import Project
from issues.models import Issue

from projects.serializers import ProjectSerializer
from issues.serializers import ProjectIssuesSerializer, UpdateProjectIssuesSerializer
from issues.serializers import CommentSerializer

# Create your views here.


class ProjectIssuesList(APIView):
    """
    List all issues for a given project
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        project = self.get_object(pk=pk)
        list_contributors = project.contributors.all()
        if not request.user in list_contributors:
            return Response({
                "message": "You are not authorized to view issues for this project, because you are not a contributor in this project"
            })
        issues = project.issues.all()
        if not issues:
            return Response({"message": "There are not issues to this project."},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectIssuesSerializer(issues, many=True)

        return Response({"Project name": project.title,
                         "issues": serializer.data})

    def post(self, request, pk, format=None):
        project = self.get_object(pk=pk)
        # check if the current user is associate to the project
        list_contributors = project.contributors.all()
        if not request.user in list_contributors:
            return Response({
                "message": "You are not authorized to create an issue, because you are not a contributor in this project"
            })
        serializer = ProjectIssuesSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors)
        issue = serializer.save(author=request.user, project=project)

        return Response({"Project name": project.title,
                         "issue name added": issue.title})


class ProjectIssuesDetail(APIView):
    """
    List all issues for a given project
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def put(self, request, pk_project, pk_issue, format=None):
        project = self.get_object(pk_project)
        try:
            issue = project.issues.get(pk=pk_issue)
        except Issue.DoesNotExist:
            return Response({"message": "This  issue doesn't exist in this project."},
                            status=status.HTTP_404_NOT_FOUND)
        if request.user == issue.author or request.user == issue.assignee:
            print('The current user is either the author or assignee')

            serializer = UpdateProjectIssuesSerializer(
                issue, data=request.data)
            if serializer.is_valid():
                serializer.save()
                issue = serializer.save()
                print(issue)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "message": "You are not authorized to update this issue, because you are not assignee or the author",
        })

    def delete(self, request, pk_project, pk_issue, format=None):
        project = self.get_object(pk_project)
        print(project)
        try:
            issue = project.issues.get(pk=pk_issue)
        except Issue.DoesNotExist:
            return Response({"message": "This  issue doesn't exist in this project."},
                            status=status.HTTP_404_NOT_FOUND)
        print(issue)
        if request.user == issue.author:
            print('The current user is the author of this issue')
            try:
                issue.delete()
            except ProtectedError:
                return Response({"message": "This issue can't be deleted!!"},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Issue Removed Successfully from the project."},
                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "You are not allowed to remove an issue from this project. Only author can remove an issue"},
                            status=status.HTTP_403_FORBIDDEN)


class CommentList(APIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk_project, pk_issue, format=None):
        project = self.get_object(pk=pk_project)
        list_contributors = project.contributors.all()
        if not request.user in list_contributors:
            return Response({
                "message": "You are not authorized to view comments for this project, because you are not a contributor in this project", },
                status=status.HTTP_403_FORBIDDEN)
        try:
            issue = project.issues.get(pk=pk_issue)
        except Issue.DoesNotExist:
            return Response({"message": "The id issue doesn't exist in database."},
                            status=status.HTTP_404_NOT_FOUND)
        comments = issue.comments.all()
        if not comments:
            return Response({"message": "There are not comments to this issue."},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comments, many=True)

        return Response({"Project name": project.title,
                         "Issue name": issue.title,
                         "comments": serializer.data})

    def post(self, request, pk_project, pk_issue, format=None):
        project = self.get_object(pk=pk_project)
        # check if the current user is associate to the project
        list_contributors = project.contributors.all()
        if not request.user in list_contributors:
            return Response({
                "message": "You are not authorized to create a comment, because you are not a contributor in this project"
            })
        print(project)
        try:
            issue = project.issues.get(pk=pk_issue)
        except Issue.DoesNotExist:
            return Response({"message": "The id issue doesn't exist in database."},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        comment = serializer.save(author_id=request.user, issue_id=issue)
        return Response({"Project name": project.title,
                         "Issue name": issue.title,
                         "comment": serializer.data})
