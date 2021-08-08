from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from projects.models import Contributor, Project


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


class ContributorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Contributor
        fields = ['user', 'project', 'role']


class ProjectSerializer(serializers.ModelSerializer):
    contributors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='username'
    )

    def get_fields(self, *args, **kwargs):
        fields = super(ProjectSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PUT":
            fields['title'].required = False
            fields['description'].required = False
        return fields

    class Meta:
        model = Project
        fields = '__all__'

    def create(self, validated_data):
        project = Project.objects.create(**validated_data)
        current_user = self.context['request'].user
        c1 = Contributor.objects.create(
            project=project, user=current_user, role='creator')
        c1.save()
        return project


class AddUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
