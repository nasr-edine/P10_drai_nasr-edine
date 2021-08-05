from django.db.models.fields import CharField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.models import User
from projects.models import Project
from projects.models import Contributor

from rest_framework.response import Response
from rest_framework import status
from django.http import Http404


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
        fields = ['user', 'project', 'role']


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
    # contributor = ContributorSerializer
    # contributor = ContributorSerializer()
    # contributor = ContributorSerializer()
    # fields = ['contributor', 'username']
    # fields = ['username', 'role']

    # def create(self, validated_data):

    #     print('create is called')
    #     print(validated_data)
    #     profile_data = validated_data.pop('username')
    #     print(profile_data)
    #     print(self.context['pk'])
    #     pk = self.context['pk']
    #     try:
    #         project = Project.objects.get(pk=pk)
    #     except Project.DoesNotExist:
    #         raise Http404
    #     try:
    #         user = User.objects.get(username=profile_data)
    #     except User.DoesNotExist:
    #         raise Http404
    #     print(user)
    #     contributors = project.contributors.all()
    #     if not user in contributors:
    #         project.contributors.add(user)
    #         contributor = Contributor.objects.get(
    #             project=project, user=user)
    #         print(contributor)
    #         contributor.role = 'contributor'
    #         contributor.save()
    #     else:
    #         raise Http404
    #     return user
    # return Response({"Success": "msb blablabla"}, status=status.HTTP_201_CREATED)


class ReadWriteSerializerMixin(object):
    read_serializer_class = None
    write_serializer_class = None

    def get_serializer_class(self):
        print(self.action)
        if self.action in ["create"]:
            return self.get_write_serializer_class()
        return self.get_read_serializer_class()

    def get_read_serializer_class(self):
        # assert self.read_serializer_class is not None, (
        #     "'%s' should either include a `read_serializer_class` attribute,"
        #     "or override the `get_read_serializer_class()` method."
        #     % self.__class__.__name__
        # )
        return ContributorSerializer

    def get_write_serializer_class(self):
        # assert self.write_serializer_class is not None, (
        #     "'%s' should either include a `write_serializer_class` attribute,"
        #     "or override the `get_write_serializer_class()` method."
        #     % self.__class__.__name__
        # )
        return AddUserSerializer
