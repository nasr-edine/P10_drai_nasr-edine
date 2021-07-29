from django.db.models.fields import CharField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.models import User
from projects.models import Project
from projects.models import Contributor


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(
        required=True
    )
    last_name = serializers.CharField(
        required=True
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'password',
                  'first_name', 'last_name', 'email']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        return user


class authorProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ContributorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Contributor
        fields = ['user', 'role']


class ProjectSerializer(serializers.ModelSerializer):
    contributors = authorProjectSerializer(many=True, read_only=True)
    title = serializers.CharField(
        required=True
    )
    description = serializers.CharField(
        required=True
    )
    type = serializers.CharField(
        required=True
    )

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'contributors']

    def create(self, validated_data):
        current_user = self.context['request'].user

        project = Project(
            title=validated_data['title'],
            description=validated_data['description'],
            type=validated_data['type']
        )
        project.save()

        c1 = Contributor.objects.create(
            project=project, user=current_user, role='creator')

        c1.save()
        return project


class AddUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
