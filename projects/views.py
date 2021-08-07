from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from projects.custompermissions import IsCreatorOrReadOnlyForContributor
from projects.models import Contributor, Project
from projects.serializers import (AddUserSerializer, ContributorSerializer,
                                  ProjectSerializer, UserSerializer)


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
            user = User.objects.get(username=request.data['username'])
        except User.DoesNotExist:
            return Response({"message": "We can't add this user because he doesn't exist in database."},
                            status=status.HTTP_404_NOT_FOUND)
        try:
            project = Project.objects.get(pk=self.kwargs['pk'])
        except Project.DoesNotExist:
            return Response({"message": "project don't exist."},
                            status=status.HTTP_404_NOT_FOUND)
        contributors = project.contributors.all()
        if user not in contributors:
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
            return Response({'message': "Yon can remove yourself from the project because you are author"},
                            status=status.HTTP_403_FORBIDDEN)
        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
