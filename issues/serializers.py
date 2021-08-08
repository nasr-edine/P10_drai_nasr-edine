from django.http.response import Http404
from rest_framework import serializers

from issues.models import Comment, Issue
from projects.models import Contributor, Project


class ProjectIssuesSerializer(serializers.ModelSerializer):
    def get_fields(self, *args, **kwargs):
        print('get_fields')
        fields = super(ProjectIssuesSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PUT":
            fields['title'].required = False
            fields['desc'].required = False
        return fields

    def create(self, validated_data):
        """
        Create and return a new `Issue` instance, given the validated data.
        """
        try:
            project = Project.objects.get(pk=self.context['view'].kwargs.get('pk_project'))
        except Project.DoesNotExist:
            raise Http404
        if 'assignee' in validated_data:
            try:
                Contributor.objects.get(user=validated_data['assignee'], project=project)
            except Contributor.DoesNotExist:
                raise serializers.ValidationError(
                    {"message": "You can not assign user: "+validated_data['assignee'].username+" "
                        "to this issue because he is not a contributor to the project: "+project.title+""})
        issue = Issue.objects.create(project=project, author=self.context['request'].user, **validated_data)
        return issue

    def update(self, instance, validated_data):
        """
        Update and return an existing `issue` instance, given the validated data.
        """
        try:
            project = Project.objects.get(pk=self.context['view'].kwargs.get('pk_project'))
        except Project.DoesNotExist:
            raise Http404
        if 'assignee' in validated_data:
            try:
                Contributor.objects.get(user=validated_data['assignee'], project=project)
            except Contributor.DoesNotExist:
                raise serializers.ValidationError(
                    {"message": "You can not assign user: "+validated_data['assignee'].username+" "
                        "to this issue because he is not a contributor to the project: "+project.title+""})
        instance.title = validated_data.get('title', instance.title)
        instance.assignee = validated_data.get('assignee', instance.assignee)
        instance.desc = validated_data.get('desc', instance.desc)
        instance.tag = validated_data.get('tag', instance.tag)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.status = validated_data.get('status', instance.status),
        instance.save()
        return instance

    class Meta:
        model = Issue
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author_id', 'issue_id', 'created_time']
