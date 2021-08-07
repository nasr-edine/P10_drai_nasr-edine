from django.db import models

from projects.models import Project, User

# Create your models here.


class Issue(models.Model):
    title = models.CharField(max_length=100, blank=False)
    desc = models.CharField(max_length=100, blank=True, default="")
    tag = models.CharField(max_length=10, blank=True, default="")
    priority = models.CharField(max_length=20, blank=True, default="")
    project = models.ForeignKey(
        Project, related_name='issues',  null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, blank=True, default="")
    created_time = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='author')
    assignee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='assignee')

    def __str__(self):
        return self.title


class Comment(models.Model):
    description = models.CharField(max_length=100)
    author_id = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    issue_id = models.ForeignKey(
        Issue, related_name='comments', on_delete=models.CASCADE, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
