from django.db import models
from django.contrib.auth.models import User

TYPES_CHOICES = [
    ("front-end", 'front-end'),
    ("back-end", 'back-end'),
    ("IOS", 'IOS'),
    ("Android", 'Android'),
]


class Project(models.Model):
    title = models.CharField(max_length=50, blank=False)
    contributors = models.ManyToManyField(
        User,
        through='Contributor',
    )
    description = models.CharField(max_length=500, blank=True, default="")
    type = models.CharField(
        max_length=20,
        choices=TYPES_CHOICES,
        blank=True,
        default="")

    unique_together = [['title', 'contributors']]

    def __str__(self):
        return self.title


class Contributor(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # inviter = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name="contributor_invites",
    # )
    role = models.CharField(max_length=20)
    # project = models.ForeignKey(
    #     Project, on_delete=models.CASCADE, related_name='contributors')

    class Meta:
        unique_together = ['project', 'user']

    # todo permission read/write for contributor and not right for  another user

    def __str__(self):
        return '%s: %s' % (self.user.username, self.project)

    # todo new app ticket
    # todo ticket
    # todo comment/issue
