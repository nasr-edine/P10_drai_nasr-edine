
# Serialize and Deserialize a user

# serialize a user
from projects.models import Project
from projects.serializers import ProjectSerializer
from projects.serializers import UserSerializer
# ringo = User.objects.create(username="Ringo Starr")
ringo = User(username='Ringo_Starr', email='ringo@example.com')
user_serializer = UserSerializer(ringo)
user_serializer.data
# from rest_framework.renderers import JSONRenderer
json = JSONRenderer().render(user_serializer.data)
# b'{"id":4,"username":"Ringo Starr","email":""}'

# Deserializing a user
# import io
# from rest_framework.parsers import JSONParser
stream = io.BytesIO(json)
data = JSONParser().parse(stream)
# {'id': 4, 'username': 'Ringo Starr', 'email': ''}
user_serializer = UserSerializer(data=data)
user_serializer.is_valid()
user_serializer.validated_data
user = user_serializer.save()

****************************************************
# Serialize and Deserialize a project
# get a project object
drf = Project.objects.get(title="DRF")

# Serialize
project_serializer = ProjectSerializer(drf)
project_serializer.data
json = JSONRenderer().render(user_serializer.data)

# Deserialize a project
stream = io.BytesIO(json)
data = JSONParser().parse(stream)
project_serializer = ProjectSerializer(data=data)
project_serializer.is_valid()
project_serializer.validated_data

project = project_serializer.save()
****************************************************

contributor = Contributor.objects.get(pk=8)
contributor_serializer = ContributorSerializer(contributor)
contributor_serializer.data
json = JSONRenderer().render(contributor_serializer.data)

stream = io.BytesIO(json)
data = JSONParser().parse(stream)
contributor_serializer = ContributorSerializer(data=data)
contributor_serializer

contributor_serializer.is_valid()
contributor_serializer.errors
contributor_serializer.validated_data
****************************************************

# from issues.models import Issue
issue = Issue(title='A big problem !')
issue = Issue.objects.get(title='A big problem !')

# from django.contrib.auth.models import User
ringo = User.objects.create(username="ringo")
ringo = User.objects.get(username="ringo")
issue.author = ringo
issue.save()

# from projects.models import Project
drf = Project.objects.create(title="DRF")
drf = Project.objects.get(title="DRF")
issue.project = drf
issue.save()


# add a user (assignee) to the issue
john = User.objects.create(username="john")
john = User.objects.get(username="john")
issue.assignee = john
issue.save()

george = User.objects.create(username="george")
george = User.objects.get(username="george")

new_assignement = ringo.assignee.create(assignee=issue2)

User.objects.create(user=john, issue=issue)


# get all issue for a given project
drf.issue_set.all()  # without related name
drf.issues.all()    # with related name
****************************************************

# list queries for django shell
# from issues.models import Issue
issue = Issue.objects.get(title__startswith='A big')
issue2 = Issue.objects.get(title__startswith='A Second')

# from issues.serializers import ProjectIssuesSerializer
serializer = ProjectIssuesSerializer(issue)
serializer.data

# from rest_framework.renderers import JSONRenderer
json = JSONRenderer().render(serializer.data)
json

# import io
# from rest_framework.parsers import JSONParser
stream = io.BytesIO(json)
data = JSONParser().parse(stream)
serializer = ProjectIssuesSerializer(data=data)
serializer.is_valid()
serializer.validated_data
issue = serializer.save()
****************************************************


# from projects.models import User
ringo = User.objects.create(username="ringo")
ringo = User.objects.get(username="ringo")
ringo
# from projects.models import Project
spring = Project.objects.create(title="spring")
spring = Project.objects.get(title="spring")
# from projects.models import Contributor
c1 = Contributor.objects.create(project=spring, user=ringo, role='creator')

issue = spring.issues.create(title="First problem", author=ringo, assignee=ringo)
issue = spring.issues.get(title="First problem")

# from issues.models import Comment
comment = issue.comments.create(description="This problem is very hard", author_id=ringo)