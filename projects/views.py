# from django.shortcuts import render, get_object_or_404
# from django.http import JsonResponse
# import json
from rest_framework import generics

from projects.models import Project
from projects.serializers import ProjectSerializer
from rest_framework.permissions import IsAuthenticated


class ProjectList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


# Create your views here.


# MAX_OBJECTS = 20


# @csrf_exempt
# def projects_list(request):
#     if request.method == 'GET':
#         projects = Project.objects.all()[:MAX_OBJECTS]
#         data = {'results': list(projects.values(
#             'title', 'description', 'type', 'author_user_id__username'))}
#         return JsonResponse(data)

#     # elif request.method == 'POST':
#     #     project_data = json.loads(request.body.decode("utf-8"))
# # @csrf_exempt


# def projects_detail(request, pk):
#     project = get_object_or_404(Project, pk=pk)
#     data = {
#         'results': {
#             'title': project.title,
#             'description': project.description,
#             'type': project.type,
#             'author_user_id': project.author_user_id.username,
#         }
#     }
#     return JsonResponse(data)
