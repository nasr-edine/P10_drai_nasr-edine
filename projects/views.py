from rest_framework import generics

from projects.serializers import ProjectSerializer
from projects.serializers import UserSerializer
from projects.serializers import ContributorSerializer
from projects.serializers import AddUserSerializer

from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView
from django.db.models import ProtectedError

from projects.models import Project
from projects.models import Contributor


class RegisterAPI(generics.CreateAPIView):
    """
    Create a new user.
    """
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully. Now perform Login to get your token",
        })


class ProjectList(generics.ListCreateAPIView):
    """
    List all projects for current user, or create a new project.
    """
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def list(self, request):
        queryset = Project.objects.filter(
            contributors=request.user)
        if queryset:
            serializer = ProjectSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response({
            "message": "You have not project actually",
        })


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a project instance.
    """
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        project = self.get_object(pk=pk)
        serializer = ProjectSerializer(project)
        list_contributors = project.contributors.all()
        if request.user in list_contributors:
            return Response(serializer.data)
        return Response({
            "message": "You are not authorized to view detail of this project, because you are not registred in this project"
        })

    def put(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)
        list_contributors = project.contributors.all()
        if request.user in list_contributors:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "message": "You are not authorized to update this project, because you are not registred in",
        })

    def delete(self, request, pk, format=None):
        project = self.get_object(pk)
        list_contributors = project.contributors.all()
        creator = User.objects.filter(
            project=project, contributor__role='creator')
        # if request.user in list_contributors:
        if not request.user in creator:
            return Response({
                "message": "You are not authorized to delete this project, because you are not the creator",
            }, status=status.HTTP_403_FORBIDDEN)
        project.delete()
        return Response({"message": "Project Deleted Successfully."},
                        status=status.HTTP_204_NO_CONTENT)


# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class ProjectContributorsList(APIView):
    """
    List all contributors for a given project, or add a new user to a given project.
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
        contributors = project.contributors.all()
        contributors2 = Contributor.objects.filter(project=project)
        serializer2 = ContributorSerializer(contributors2, many=True)

        print(contributors2)
        if not contributors:
            return Response({"message": "There are not contributors to this project."},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(contributors, many=True)
        return Response({"Project name": project.title,
                         "contributors": serializer2.data})

    def post(self, request, pk, format=None):
        project = self.get_object(pk=pk)
        try:
            creator = User.objects.filter(
                project=project, contributor__role='creator')
        except User.DoesNotExist:
            return Response({"message": "There are not creator for this project save in database."},
                            status=status.HTTP_404_NOT_FOUND)
        if request.user in creator:
            serializer = AddUserSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    user = User.objects.get(
                        username=serializer.data['username'])
                except User.DoesNotExist:
                    return Response({"message": "We can't add this user because he doesn't exist in database."},
                                    status=status.HTTP_404_NOT_FOUND)
                contributors = project.contributors.all()
                if not user in contributors:
                    project.contributors.add(user)
                else:
                    return Response({"message": "This user is already added to the project."},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors)
            return Response({"Project name": project.title,
                             "user to add": user.username})
        else:
            return Response({"message": "You are not allowed to add a user to this project. Only the creator can add a new user"},
                            status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk_project, pk_user, format=None):
        project = self.get_object(pk=pk_project)
        try:
            creator = User.objects.filter(
                project=project, contributor__role='creator')
        except User.DoesNotExist:
            return Response({"message": "There are not creator for this project save in database."},
                            status=status.HTTP_404_NOT_FOUND)
        if request.user in creator:
            print(project)
            try:
                contributor = project.contributors.get(pk=pk_user)
            except User.DoesNotExist:
                return Response({"message": "This  user doesn't exist in this project."},
                                status=status.HTTP_404_NOT_FOUND)

            try:
                project.contributors.remove(contributor)
            except ProtectedError:
                return Response({"message": "This user can't be deleted!!"},
                                status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "User Removed Successfully from the project."},
                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "You are not allowed to remove a user from this project. Only the creator can remove a user"},
                            status=status.HTTP_403_FORBIDDEN)
