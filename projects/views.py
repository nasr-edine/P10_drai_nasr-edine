# from rest_framework.exceptions import NotFound
from django import http
from rest_framework import generics

from projects.serializers import ProjectSerializer
from projects.serializers import UserSerializer
from projects.serializers import ContributorSerializer
from projects.serializers import AddUserSerializer
from projects.serializers import ReadWriteSerializerMixin

from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from django.db.models import ProtectedError

from projects.models import Project
from projects.models import Contributor

from projects.custompermissions import IsCreatorOrReadOnlyForContributor


class RegisterAPI(generics.CreateAPIView):
    """
    Create a new user.
    """
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT
                            )
        user = serializer.save()

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully. Now perform Login to get your token"},
            status=status.HTTP_201_CREATED)


class ProjectList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.filter(
            contributors=self.request.user)
        return queryset


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsCreatorOrReadOnlyForContributor]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectContributorsList2(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsCreatorOrReadOnlyForContributor]
    serializer_class = ContributorSerializer

    def get_queryset(self):
        project = Project.objects.get(pk=self.kwargs['pk'])
        queryset = Contributor.objects.filter(project=project)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = AddUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(username=serializer.data['username'])
        except User.DoesNotExist:
            return Response({"message": "We can't add this user because he doesn't exist in database."},
                            status=status.HTTP_404_NOT_FOUND)
        try:
            project = Project.objects.get(pk=self.kwargs['pk'])
        except Project.DoesNotExist:
            return Response({"message": "project don't exist."},
                            status=status.HTTP_404_NOT_FOUND)
        contributors = project.contributors.all()
        if not user in contributors:
            c1 = Contributor.objects.create(
                project=project, user=user, role='contributor')
            c1.save()
            return Response(ContributorSerializer(c1).data)
        else:
            return Response({"message": "This user is already added to the project."},
                            status=status.HTTP_400_BAD_REQUEST)


class ProjectContributorDestroy(generics.DestroyAPIView):

    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all()
    permission_classes = [IsAuthenticated, IsCreatorOrReadOnlyForContributor]

    def delete(self, request, pk, pk_user, format=None):
        try:
            project = Project.objects.get(pk=self.kwargs['pk'])
        except Project.DoesNotExist:
            raise Http404
        try:
            user = User.objects.get(pk=self.kwargs['pk_user'])
        except User.DoesNotExist:
            raise Http404
        try:
            contributor = Contributor.objects.get(
                project=project, user=user)
        except Contributor.DoesNotExist:
            raise Http404
        if contributor.role == 'creator':
            return Response({'message': "Yon can remove yourself from the project because you are author"}, status=status.HTTP_403_FORBIDDEN)
        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class ProjectContributorsList(APIView):
#     """
#     List all contributors for a given project, or add a new user to a given project.
#     """
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self, pk):
#         try:
#             return Project.objects.get(pk=pk)
#         except Project.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         project = self.get_object(pk=pk)
#         contributors = project.contributors.all()
#         contributors2 = Contributor.objects.filter(project=project)
#         # contributors2.role = 'contributor'
#         serializer2 = ContributorSerializer(contributors2, many=True)
#         # serializer2.save()
#         print(contributors2)
#         if not contributors:
#             return Response({"message": "There are not contributors to this project."},
#                             status=status.HTTP_404_NOT_FOUND)
#         serializer = UserSerializer(contributors, many=True)
#         return Response({"Project name": project.title,
#                          "contributors": serializer2.data})

#     def post(self, request, pk, format=None):
#         project = self.get_object(pk=pk)
#         try:
#             creator = User.objects.filter(
#                 project=project, contributor__role='creator')
#         except User.DoesNotExist:
#             return Response({"message": "There are not creator for this project save in database."},
#                             status=status.HTTP_404_NOT_FOUND)
#         if request.user in creator:
#             serializer = AddUserSerializer(data=request.data)
#             if serializer.is_valid():
#                 try:
#                     user = User.objects.get(
#                         username=serializer.data['username'])
#                 except User.DoesNotExist:
#                     return Response({"message": "We can't add this user because he doesn't exist in database."},
#                                     status=status.HTTP_404_NOT_FOUND)
#                 contributors = project.contributors.all()
#                 if not user in contributors:
#                     project.contributors.add(user)
#                     contributor = Contributor.objects.get(
#                         project=project, user=user)
#                     contributor.role = 'contributor'
#                     contributor.save()
#                 else:
#                     return Response({"message": "This user is already added to the project."},
#                                     status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response(serializer.errors)
#             return Response({"Project name": project.title,
#                              "user added": UserSerializer(user).data})
#         else:
#             return Response({"message": "You are not allowed to add a user to this project. Only the creator can add a new user"},
#                             status=status.HTTP_403_FORBIDDEN)

#     def delete(self, request, pk_project, pk_user, format=None):
#         project = self.get_object(pk=pk_project)
#         try:
#             creator = User.objects.filter(
#                 project=project, contributor__role='creator')
#         except User.DoesNotExist:
#             return Response({"message": "There are not creator for this project save in database."},
#                             status=status.HTTP_404_NOT_FOUND)
#         if request.user in creator:
#             print(project)
#             try:
#                 contributor = project.contributors.get(pk=pk_user)
#             except User.DoesNotExist:
#                 return Response({"message": "This  user doesn't exist in this project."},
#                                 status=status.HTTP_404_NOT_FOUND)

#             try:
#                 project.contributors.remove(contributor)
#             except ProtectedError:
#                 return Response({"message": "This user can't be deleted!!"},
#                                 status=status.HTTP_400_BAD_REQUEST)

#             return Response({"message": "User Removed Successfully from the project."},
#                             status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response({"message": "You are not allowed to remove a user from this project. Only the creator can remove a user"},
#                             status=status.HTTP_403_FORBIDDEN)
