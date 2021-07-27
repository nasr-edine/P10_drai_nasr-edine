from rest_framework import serializers

from django.contrib.auth.models import User
from projects.models import Project
from projects.models import Contributor


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'])
        return user


class ContributorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Contributor
        fields = ['user', 'role']


class ProjectSerializer(serializers.ModelSerializer):
    contributors = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'contributors']

    def create(self, validated_data):
        current_user = self.context['request'].user

        project = Project(
            title=validated_data['title'],
            # description=validated_data['description'],
            type=validated_data['type']
        )
        project.save()

        c1 = Contributor.objects.create(
            project=project, user=current_user, role='creator')

        c1.save()
        return project


class AddUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
