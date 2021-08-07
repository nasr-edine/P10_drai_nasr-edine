from rest_framework import serializers

# from django.contrib.auth.models import User
from issues.models import Comment, Issue

# from projects.models import Contributor


class ProjectIssuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'project', 'author', 'assignee']
        # read_only_fields = ['author']


class UpdateProjectIssuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'desc', 'project',
                  'author', 'assignee', 'created_time']
        read_only_fields = ['author', 'project', 'created_time']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class UpdateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'description', 'author_id',
                  'issue_id', 'created_time']
        read_only_fields = ['author_id', 'issue_id', 'created_time']
