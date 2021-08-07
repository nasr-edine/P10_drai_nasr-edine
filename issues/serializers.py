from rest_framework import serializers

from issues.models import Comment, Issue
from projects.models import Contributor, Project


class ProjectIssuesSerializer(serializers.ModelSerializer):

    def validate(self, data):
        """
        Check that the assignee user is a project contributor.
        """
        project = Project.objects.get(pk=self.context.get("project_id"))
        user = data['assignee']
        try:
            Contributor.objects.get(user=user, project=project)
        except Contributor.DoesNotExist:
            raise serializers.ValidationError({"message": "You can not assign this user to this issue, \
                             because he is not a contributor to the project"})
        return data

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
