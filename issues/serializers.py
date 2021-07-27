from rest_framework import serializers

# from django.contrib.auth.models import User
from issues.models import Issue
from issues.models import Comment
# from projects.models import Contributor


class ProjectIssuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'project', 'author', 'assignee']
        # read_only_fields = ['author']


class UpdateProjectIssuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'project',
                  'author', 'assignee', 'created_time']
        read_only_fields = ['author', 'project', 'created_time']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
