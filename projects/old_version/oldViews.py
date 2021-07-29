class ProjectList(generics.ListCreateAPIView):
    """
    List all projects for current user, or create a new project.
    """
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    # todo def get_queryset(self):
    # return super().get_queryset()
    # def get_queryset(self):
    #         return Project.objects.filter(contributors=self.request.user).all()
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
