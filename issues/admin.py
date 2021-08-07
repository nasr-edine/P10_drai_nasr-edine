from django.contrib import admin

from issues.models import Comment, Issue

# Register your models here.
admin.site.register(Issue)
admin.site.register(Comment)
