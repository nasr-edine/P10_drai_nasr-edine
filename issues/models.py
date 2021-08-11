from django.db import models

from projects.models import Project, User

TAGS_CHOICES = [
    ("bug", 'bug'),
    ("tache", 'tache'),
    ("amelioration", 'amelioration'),
]
STATUSES_CHOICES = [
    ('todo', 'todo'),
    ('inprogress', 'inprogress'),
    ('open', 'open'),
    ('closed', 'closed'),
    ('reopened', 'reopened'),
    ('resolved', 'resolved'),
]
PRIORITIES_CHOICES = [
    ('highest', 'highest'),
    ('high', 'high'),
    ('medium', 'medium'),
    ('low', 'low'),
]


class Issue(models.Model):
    title = models.CharField(max_length=100, blank=False)
    desc = models.CharField(max_length=200, blank=False)
    tag = models.CharField(
        max_length=20,
        choices=TAGS_CHOICES,
        blank=True,
        default="bug")
    priority = models.CharField(
        max_length=20,
        choices=PRIORITIES_CHOICES,
        blank=True,
        default="medium")
    project = models.ForeignKey(
        Project, related_name='issues',  null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=STATUSES_CHOICES,
        blank=True,
        default="todo")
    created_time = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='author')
    assignee = models.ForeignKey(
        User,
        null=True,
        blank=True,
        default="",
        on_delete=models.CASCADE,
        related_name='assignee')

    def __str__(self):
        return self.title


class Comment(models.Model):
    description = models.CharField(max_length=200, blank=False)
    author_id = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    issue_id = models.ForeignKey(
        Issue, related_name='comments', on_delete=models.CASCADE, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
