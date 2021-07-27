from projects.models import Project, Contributor

from django.contrib.auth.models import User

ringo = User.objects.create(username="Ringo Starr")
ringo = User.objects.get(username="Ringo Starr")
ringo

paul = User.objects.create(username="Paul McCartney")
paul = User.objects.get(username="Paul McCartney")

paul

# create a new project
drf = Project.objects.create(title="DRF")
drf = Project.objects.get(title="DRF")

drf

c1 = Contributor.objects.create(project=drf, user=ringo, role='creator')
c1 = Contributor.objects.get(project=drf, user=ringo, role='creator')

*** print all contributors for a given project ** *
drf.contributors.all()

c2 = Contributor.objects.create(project=drf, user=paul, role='contributor')

john = User.objects.create(username="John Lennon")

# add a contributor
john = User.objects.create(username="John Lennon")
drf.contributors.add(john, through_defaults={'role': 'contributor'})

drf.contributors.create(name="George Harrison",
                        through_defaults={'role': 'contributor'})

# remove a contributor
drf.contributors.remove(ringo)

# add an instance from the intermediate model:
Contributor.objects.create(project=drf, user=ringo, role='creator')


# view the relationship
Contributor.objects.all()

# find all projects with a contributor whose name start with 'ringo'
Project.objects.filter(contributors__username__startswith='ringo')


User.objects.filter(project__title='DRF', contributor__role__gt='creator')


drf.contributors.get(username="Ringo Starr")
Contributor.objects.get(user=ringo, project=drf)

# Access to an instance of intermediate model
ringos_contributor = Contributor.objects.get(project=drf, user=ringo)

# Access to creator from a project
User.objects.filter(project__title='DRF', contributor__role='creator')

# Acces all contributors from a project
User.objects.filter(project__title='DRF', contributor__role='contributor')
