from django.http.response import Http404
from rest_framework import serializers

from issues.models import Comment, Issue
from projects.models import Contributor, Project


class ProjectIssuesSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        """
        Update and return an existing `issue` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.assignee = validated_data.get('assignee', instance.assignee)
        try:
            project = Project.objects.get(pk=self.context['view'].kwargs.get('pk_project'))
        except Project.DoesNotExist:
            raise Http404
        try:
            Contributor.objects.get(user=instance.assignee, project=project)
        except Contributor.DoesNotExist:
            raise serializers.ValidationError(
                {"message": "You can not assign user: "+validated_data['assignee'].username+" "
                    "to this issue because he is not a contributor to the project: "+project.title+""})

        instance.desc = validated_data.get('desc', instance.desc)
        instance.save()
        return instance

    def create(self, validated_data):
        """
        Create and return a new `Issue` instance, given the validated data.
        """
        try:
            project = Project.objects.get(pk=self.context['view'].kwargs.get('pk_project'))
        except Project.DoesNotExist:
            raise Http404
        try:
            Contributor.objects.get(user=validated_data['assignee'], project=project)
        except Contributor.DoesNotExist:
            raise serializers.ValidationError(
                {"message": "You can not assign user: "+validated_data['assignee'].username+" "
                    "to this issue because he is not a contributor to the project: "+project.title+""})
        issue = Issue(
            title=validated_data['title'],
            assignee=validated_data['assignee'],
            project=project,
            author=self.context['request'].user)
        issue.save()
        return issue

    class Meta:
        model = Issue
        fields = ['id', 'title', 'project', 'author', 'assignee']


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
